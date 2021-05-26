import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '@/Main.vue'

// 스터디 모집 생성
import StudyCreate from '@/views/StudyRecruitment/StudyCreate.vue'

// 스터디 모집 리스트
import StudyList from '@/views/StudyRecruitment/StudyList.vue'

// 스터디 모집 디테일 페이지
import StudyDetail from '@/views/StudyRecruitment/StudyDetail.vue'

// 스터디 모집 수정
import StudyUpdate from '@/views/StudyRecruitment/StudyUpdate.vue'

// 게시판 페이지
import BoardDetail from '@/views/Board/BoardDetail.vue'
import BoardList from '@/views/Board/BoardList.vue'
import BoardCreate from '@/views/Board/BoardCreate.vue'


// 로그인
import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
//마이페이지
import MyPage from '@/views/MyPage.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  // 스터디 모집
  {
    path: '/studycreate',
    name: 'StudyCreate',
    component: StudyCreate
  },
  {
    path: '/studylist',
    name: 'StudyList',
    component: StudyList
  },
  {
    path: '/studyupdate',
    name: 'StudyUpdate',
    component: StudyUpdate
  },
  {
    path: '/studydetail',
    name: 'StudyDetail',
    component: StudyDetail
  },
  //게시판 페이지
  {
    path: '/boarddetail',
    name: 'BoardDetail',
    component: BoardDetail
  },
  {
    path: '/boardlist',
    name: 'BoardList',
    component: BoardList
  },
  {
    path: '/boardcreate',
    name: 'BoardCreate',
    component: BoardCreate
  },
  // 로그인
  {
    path: '/login',
    name: 'Login',
    component:Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component:Signup
  },
    {
    path: '/mypage',
    name: 'MyPage',
    component:MyPage
  },
]

const router = new VueRouter({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
