<template>
  <div class="StudyDetail-container">
    <div v-if="study" class="StudyDetail-box">

      <h1 class="title bot">{{studyDetail.title}}</h1>

      <div class="subject bot">
        <h2>
          목표 과제 | {{studyDetail.subject}}
        </h2>
      </div>

      <div class="member-limit bot">
        <h2>
          모집 인원 | {{studyDetail.member_limit}}
        </h2>
      </div>

      <div class="needmoney bot">
        <h2>
          참여 금액 | {{studyDetail.needmoney}}
        </h2>
      </div>

      <div class="needmoney bot">
        <h2>
          시작일~종료일 | {{studyDetail.start[0]}} ~ {{studyDetail.end[0]}}
        </h2>
      </div>

      <div class="content bot">
        <h3>{{studyDetail.content}}</h3>
      </div>
      <!-- 버튼 -->
      <!-- 마스터 -->
      <div v-if="studyMaster" class="btn-group">
        <div class="btn" @click="update"> 수정하기 </div>
        <div class="btn" @click="confirm"> 지원마감 </div>
        <div class="btn" @click="deleteModalChange"> 삭제하기 </div>
        <div class="btn" @click="locationBack"> 뒤로가기 </div>
      </div>
      <!-- 지원자 -->
      <div v-else class="btn-group">
        <div v-if="applyCheck" class="btn" @click="apply"> 신청취소 </div>
        <div v-else class="btn" @click="apply"> 신청하기 </div>
        <div class="btn" @click="locationBack"> 뒤로가기 </div>
      </div>
    </div>
    <div v-if="deleteModal" class="delete-modal">
      <div  class="delete-modal-box">
        <div class="modal-title">정말로 삭제하시 겠습니까?</div>
        <div class="btn-group">
          <i @click="deleteStudy" class="btn fas fa-trash-alt"></i>
          <i @click="deleteModalChange" class="btn fas fa-times-circle"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      study : false,
      studyDetail : null,
      studyId: this.$route.query.title,
      studyMaster:false,
      applyCheck : false,
      deleteModal : false,
    }
  },
  methods: {
    getStudyDetail() {
      const userId = parseInt(localStorage.getItem('user_id'))
      const config = this.setToken()
      axios.get(`https://k4b205.p.ssafy.io:7799/study/${this.studyId}/`,config)
      .then((res)=>{
        this.studyDetail = res.data
        this.studyDetail.start = [
          this.studyDetail.start.substring(0,10),
          this.studyDetail.start.substring(11,16)
        ]
        this.studyDetail.end = [
          this.studyDetail.end.substring(0,10),
          this.studyDetail.end.substring(11,16)
        ]
        this.study = true
        if (this.studyDetail.master === userId) {
          this.studyMaster = true
        } else {
          if (this.studyDetail.applied) {
            this.applyCheck = true
          } else{
            this.applyCheck = false
          }
        }
      })
    },
    apply(){
      const data = {
        "study" : this.studyId,
      }
      const config = this.setToken()
      axios.post('https://k4b205.p.ssafy.io:7799/apply/', data, config)
      .then((res)=>{
        if (res.data === 'apply success') {
          this.applyCheck = true
          alert('신청되었습니다.')
        } else{
          this.applyCheck = false
          alert('신청이 취소되었습니다.')
        }
        this.getStudyDetail()
      })
    },
    locationBack(){
      history.go(-1)
    },
    update () {
      this.$router.push({
        name: 'StudyUpdate',
        query : this.studyDetail
      })
    },
    confirm () {
      const config = this.setToken()
      const num = parseInt(this.studyId)
      const user = {
        'id' : parseInt(localStorage.getItem('username')),
        'username' : localStorage.getItem('username'),
        'email' : localStorage.getItem('email'),
      }
      axios.post(`https://k4b205.p.ssafy.io:7799/confirm/${num}/`,user, config)
      .then(()=>{
        alert('지원 마감 되었습니다.')
        this.$router.push({name: "MyPage"})
      })
    },
    deleteStudy () {
      const config = this.setToken()
      const num = parseInt(this.studyId)
      axios.delete(`https://k4b205.p.ssafy.io:7799/study/${num}/`, config)
      .then(()=>{
        alert('삭제되었습니다.')
        this.$router.push({name: "MyPage"})
      })
    },
    deleteModalChange () {
      this.deleteModal = !this.deleteModal
    },
    setToken () {
      const token = localStorage.getItem('jwt')
      const config = {
        headers: {
          Authorization : `Token ${token}`,
        }
      }
      return config
    },
  },
  mounted() {
    window.scrollTo(0,0)
    this.getStudyDetail()
  },
}
</script>

<style scoped>
h1, h2, h3{
  margin: 0;
}
.StudyDetail-container{
  width: 100%;
  display: flex;
  min-height: 100vh;
  justify-content: center;
  padding-bottom: 10vh;
  backdrop-filter: saturate(180%) blur(3px);
}
.StudyDetail-container .delete-modal {
  width: 100%;
  height: 100vh;
  position: absolute;
  top: 0%;
  left: 0%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, .7);
  backdrop-filter: saturate(180%) blur(5px);
}
.StudyDetail-container .delete-modal .delete-modal-box{
  width: 50%;
  height: 17%;
  text-align: center;
  background: white;
  border-radius: 20px;
}
.StudyDetail-container .delete-modal .delete-modal-box .modal-title{
  margin: 20px;
  font-size: 1.5rem;
}
.StudyDetail-container .delete-modal .btn-group .btn{
  font-size: 1.5rem;
}

.StudyDetail-container .StudyDetail-box{
  width: 80vw;
  margin-top: 30px;
}
.StudyDetail-container .StudyDetail-box .bot{
  border-bottom: 1px black solid;
  padding: 20px 0;
}
.StudyDetail-container .btn-group{
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}
.StudyDetail-container .btn-group .btn{
  transition: ease 1s;
  font-size: 1.3rem;
}
.StudyDetail-container .btn-group .btn:hover{
  cursor: pointer;
  transform: scale(1.1);
}
</style>