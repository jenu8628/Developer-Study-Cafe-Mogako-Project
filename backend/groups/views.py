from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from board.models import Board
from accounts.models import User
from .models import Group, Study, Apply
from .serializers import GroupSerializer, StudySerializer, ApplySerialier ,MemberSerializer
import datetime


class StudyViewSet(viewsets.ModelViewSet):
    '''
    스터디 목록보기, 생성 및 삭제 수정 기능

    ---
    '''
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def list(self, request):
        '''
        모든 스터디들의 정보를 조회합니다. 
        '''
        queryset = Study.objects.all()
        for single_study in queryset:
            if request.user.id in StudySerializer(single_study).data['members']:
                single_study.applied = True
            else:
                single_study.applied = False
            single_study.save()

        serializer = StudySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        '''
        pk번째 스터디의 정보를 조회할 수 있습니다.
        해당 스터디에 지원한 경우, applied 필드는 true값입니다. 
        '''
        study = get_object_or_404(Study, id=pk)
        member_for_study = Apply.objects.filter(study=study, apply_user=request.user)

        if member_for_study:
            study.applied = True
        else:
            study.applied = False

        study.save()
        serializer = StudySerializer(study)

        return Response(serializer.data)

    def create(self, request):
        '''
        스터디 글을 작성합니다.
        필수 입력 값은 title, subject, content, start, end, needmoney, tech_tags, kind_tags, member_limit입니다.
        '''
        writer = request.user
        data = request.data
        
        if data['needmoney']=='':
            money=0
        else: 
            money=data['needmoney']

        if data['deposit']=='':
            deposit_money=0
        else: 
            deposit_money=data['deposit']

        if int(deposit_money) > int(writer.money):
            return Response({"보증금 보다 소유자금이 더 작습니다"})

        new_study = Study.objects.create(
            title=data['title'], subject=data['subject'], content=data['content'], master=writer, study_image=data['study_image'],
            start=data['start'], end=data['end'], needmoney=money, tech_tags=data['tech_tags'], deposit=deposit_money,
            kind_tags=data['kind_tags'],  member_limit=data['member_limit'], apply_numbers=1,
            applied=True
        )

        Apply.objects.create(study=new_study, apply_user=request.user)
        writer.money= int(writer.money)-int(deposit_money)
        writer.save()
        return Response(StudySerializer(new_study).data)
    
    def update(self, request, pk=None):
        '''
        스터디 정보를 수정할 수 있습니다. *needmoney, deposit 수정막아야함
        현재 사용자가 글 작성자 본인이 아닌 경우 오류가 발생합니다. 
        '''
        study = get_object_or_404(Study, id=pk)
        data = request.data

        if study.master != request.user:
            return Response({"access denied"})

        serializer = StudySerializer(study, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        if study.apply_numbers > serializer.validated_data['member_limit']:
            return Response({"wrong number"})

        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        스터디를 삭제합니다.
        스터디 글을 작성한 사용자만 삭제할 수 있으며, 
        스터디에 대한 게시판이 존재하는 경우 게시판과 게시판에 포함된
        글과 댓글도 전부 삭제됩니다. 
        '''
        study = get_object_or_404(Study, id=pk)
        target_board = Board.objects.filter(study=study)
        
        if study.master != request.user:
            return Response({"access denied"})

        # 보증금 분배
        members = Apply.objects.filter(
                study=pk
            )
        reward = study.deposit
    
        for member in members:
            men=User.objects.get(pk=member.apply_user.pk)
            men.money+=reward
            if study.master.pk != men.pk:
                men.money+=study.needmoney
            men.save()

        apply_users = Apply.objects.filter(study=study)
        apply_users.delete()

        if target_board.exists():
            target_board.delete()
        request.user.money+=study.deposit
        request.user.save()
        study.delete()

        return Response({"Successfully deleted"})

class ApplyViewSet(viewsets.ModelViewSet):
    '''
    스터디 지원 기능
    post를 이용하여 스터디에 지원할 수 있습니다

    ---
    '''
    queryset = Apply.objects.all()
    serializer_class = ApplySerialier

    def list(self, request):
        '''
        모든 스터디에 대한 전체 지원 현황을 조회할 수 있습니다.
        '''
        queryset = Apply.objects.all()
        serializer = ApplySerialier(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
        pk번째 스터디에 대한 사용자들의 지원 현황을 조회할 수 있습니다. 
        '''
        target_study = Study.objects.get(id=pk)
        user_for_study = Apply.objects.filter(study=target_study)
        serializer = ApplySerialier(user_for_study, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
        스터디에 지원이 가능합니다. 
        POST 요청을 보내 지원하거나 재차 요청해 취소할 수 있으며,
        각각의 경우에 따라 needmoney만큼의 값을 사용자가 가진 money에서 증감합니다.
        사용자가 가진 money의 값이 스터디의 needmoney보다 부족한 경우 오류가 발생하고,
        스터디의 member_limit와 현재 apply_numbers가 동일한 경우, 
        스터디의 지원 인원이 전부 채워진 것으로 간주해 추가로 요청을 보낼 시 오류가 발생합니다.
        '''
        target_study = Study.objects.get(id=request.data['study'])

        user_for_study = Apply.objects.filter(
            study=target_study, apply_user=request.user
        )

        if target_study.confirmed==False:
            if user_for_study.exists():

                if user_for_study[0].apply_user.id == target_study.master.id:
                    return Response({"스터디 마스터는 신청을 취소할 수 없습니다."})

                user_for_study.delete()
                target_study.apply_numbers -= 1
                target_study.applied = False
                request.user.money+=target_study.needmoney
                request.user.money+=target_study.deposit
                request.user.save()
                target_study.save()     
                return Response("Successfully deleted")
            else:
                if target_study.member_limit == target_study.apply_numbers:
                    return Response({"exceed"})
                
                if request.user.money< target_study.needmoney + target_study.deposit:
                    return Response({"금액 부족"})

                Apply.objects.create(
                    study=target_study, apply_user=request.user
                )
                request.user.money-=target_study.needmoney
                request.user.money-=target_study.deposit
                request.user.save()
                target_study.apply_numbers += 1
                target_study.applied = True
                target_study.save()
                return Response("apply success")
        else:
            return Response("스터디가 이미 진행 중입니다.")
    

class StudyConfirmView(APIView):
    '''
    모집된 스터디원들을 그룹장이 최종승인 하여 스터디 그룹을 만듭니다.

    ---
    '''
    def get(self, request, pk=None):
        apply = Apply.objects.filter(study_id=pk)
        serializer = MemberSerializer(apply, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        '''
        스터디 글을 작성한 사용자가 스터디를 승인할 수 있습니다.
        스터디가 승인되면 스터디의 confirmed 필드가 true값으로 변경되고,
        해당 스터디를 참조하는 게시판을 생성합니다.
        '''
        study = Study.objects.get(id=pk)
        
        if study.confirmed == True:
            return Response({"already confirmed"})

        apply_members = Apply.objects.filter(study=study)

        if study.master != request.user:
            return Response({"wrong"})

        new_group = Group.objects.create(
            study=study,
            start=study.start,
            end=study.end,
            master=study.master
        )

        study.confirmed = True
        study.save()
        Board.objects.create(
            study=study
        )
        return Response({"confirmed"})


class ExpireView(APIView):
    '''
    정산기능
    그룹장이 그룹 end 시간이 지난후에 post를 하면 정산됩니다.

    ---
    '''
    def get(self, request, pk=None):
        now = datetime.datetime.now()
        now_day=now.strftime('%Y-%m-%d %H:%M:%S'+'+00:00')
        group = Group.objects.get(study_id=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    # 1월 1일까지 스터디였으면 1월1일이 되면 정산버튼 활성화
    def post(self, request, pk=None):
        now = datetime.datetime.now()
        now_day=now.strftime('%Y-%m-%d %H:%M:%S'+'+00:00')
        group = Group.objects.get(study_id=pk)
        if now_day>=str(group.end) and group.ok==False:
            num=Study.objects.get(id=pk)
            count =Apply.objects.filter(study_id=pk).count()
            money=(count-1)*num.needmoney
            master=num.master
            master.money+=money
            master.save()

            # 보증금 분배
            members = Apply.objects.filter(
                    study=pk
                )
            reward = num.deposit
            
            for member in members:
                men=User.objects.get(pk=member.apply_user.pk)
                men.money+=reward
                print(men.money)
                men.save()
            group.ok=True
            group.save()
    
            return Response({"정산 완료"})
        else:
            return Response({"이미 정산되었습니다"}) 


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)


class BanView(APIView):
    '''
    /ban/{id}/의 {id}는 study_id값, 추방 아이디 apply_user값을 post로 전송
    그룹장이 그룹원을 추방합니다.
    보증금이 있을 경우 그룹원과 나눠갖습니다.

    ---
    '''
    def get(self, request, pk=None):
        apply = Apply.objects.filter(study_id=pk)
        serializer = MemberSerializer(apply, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        group = Group.objects.get(study_id=pk)
        study = Study.objects.get(id=pk)

        if study.master != request.user:
            return Response({"wrong"})
        else:
            serializer = MemberSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # 추방
                kick = Apply.objects.get(
                    study=pk, apply_user_id=serializer.data['apply_user']
                )
                kick.delete()

                # 팀원에게 보증금 분배
                members = Apply.objects.filter(
                    study=pk
                )
                reward=int(study.deposit/members.count())
                for member in members:
                    men=User.objects.get(email=member.apply_user)
                    men.money+=reward
                    men.save()
                return Response({"추방 하였습니다."})


class GiveUpView(APIView):
    '''
    진행중인 스터디를 포기합니다
    보증금이 있을 경우 돌려받지 못합니다.
    ---
    '''
    def get(self, request, pk=None):
        apply = Apply.objects.filter(study_id=pk)
        serializer = MemberSerializer(apply, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        group = Group.objects.get(study_id=pk)
        study = Study.objects.get(id=pk)

        # 스터디 포기
        apply = Apply.objects.get(study=pk, apply_user=request.user.pk)
        apply.delete()
  
        # 팀원에게 보증금 분배
        if study.master != request.user:
            if int(study.deposit) > 0:    
                members = Apply.objects.filter(
                    study=pk
                )
                reward=int(study.deposit/members.count())
                for member in members:
                    men=User.objects.get(email=member.apply_user)
                    men.money+=reward
                    men.save()
            return Response({"give up"})
            
        # 팀장이 포기할시 팀원에게 보증금을 돌려주고 팀장의 보증금이 분배됩니다
        else:
            if int(study.deposit) > 0:
                members = Apply.objects.filter(
                    study=pk
                )
                reward=int(study.deposit/members.count())+int(study.deposit)
                for member in members:
                    men=User.objects.get(email=member.apply_user)
                    men.money+=reward
                    men.save()
            return Response({"give up"})