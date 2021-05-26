<template>
  <div class="FreeStudyCreate-container">
    <div class="FreeStudyCreate-box input-font">
      <!-- 분류 -->
      <select v-model="kindTags" id="kinds" class="kinds FreeStudyCreate-element">
        <option value="" disabled hidden>분류를 선택하세요.</option>
        <option value="스터디">스터디</option>
        <option value="프로젝트">프로젝트</option>
        <option value="1:1 코칭">1:1 코칭</option>
      </select>
      <!-- 주제 선정 -->
      <select v-model="techTags" id="kinds" class="kinds FreeStudyCreate-element">
        <option value="" disabled hidden>스터디 주제를 선택하세요.</option>
        <option value="Algorithm">알고리즘</option>
        <option value="cs_study">컴퓨터사이언스</option>
        <option value="AI">인공지능</option>
        <option value="BigData">빅데이터</option>
        <option value="Game">게임</option>
        <option value="Security">보안</option>
        <option value="Embedded">임베디드</option>
        <option value="Mobile">모바일</option>
        <option value="Web">웹</option>
      </select>
      <!-- 제목 -->
      <input
        type="text"
        v-model="title" 
        class="input-font text-input FreeStudyCreate-element" 
        placeholder="제목을 입력하세요."
      >
      <!-- 주제 -->
      <input 
      type="text" 
      v-model="subject" 
      class="input-font text-input FreeStudyCreate-element" 
      placeholder="과제를 입력하세요."
      >
      <!-- 소개글 -->
      <textarea 
      name="content" 
      v-model="content" 
      class="input-font textarea-input FreeStudyCreate-element" 
      cols="30" rows="10" 
      placeholder="소개글을 입력하세요.">
      </textarea>
      <!-- 제한인원 -->
      <label for="limit">
        제한인원 :  
        <input 
        id="limit" 
        name="limit"
        min="2" v-model="limit" 
        class="input-font number-input text-input FreeStudyCreate-element" 
        type="number" placeholder="제한인원을 설정하세요."
        > 명
      </label>
      <!-- 보증금 -->
      <label for="deposit">
        보증금 :  
        <input 
        id="deposit" 
        min="0" v-model="deposit" 
        class="input-font number-input text-input FreeStudyCreate-element" 
        type="number" step="1000" 
        placeholder="참여 금액을 설정하세요"
        > 원
      </label>
      <div class="explanation">*보증금은 참여인원 모두가 지불하며, 그룹 종료일에 맞춰 1/N로 정산됩니다. 단, 중도포기나 추방당할 시에는 돌려받지 못합니다.</div>
      <!-- 수강료 -->
      <label for="needmoney">
        수강료 :  
        <input 
        id="needmoney" 
        min="0" v-model="needmoney" 
        class="input-font number-input text-input FreeStudyCreate-element" 
        type="number" step="10000" 
        placeholder="참여 금액을 설정하세요"
        > 원
      </label>
      <div class="explanation">*수강료는 지원하는 인원이 그룹장에게 지불하는 비용으로, 0원부터 설정 가능합니다.</div>
      <!-- 시작일 -->
      <label for="start" >
        시작일 : 
        <input 
        type="date" id="start" 
        class="input-font date-input text-input FreeStudyCreate-element" 
        v-model="start"
        >
      </label>
      <!-- 종료일 -->
      <label for="end">
        종료일 : 
        <input 
        type="date" id="end" 
        class="input-font date-input text-input FreeStudyCreate-element" 
        v-model="end"
        >
      </label>

      <div class="btn-box">
        <i @click="studyCreate" class="FreeStudyCreate-btn fas fa-check-circle"></i>
        <i @click="locationBack" class="FreeStudyCreate-btn fas fa-times-circle"></i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import '@/assets/css/create.css'

export default {
  data() {
    return {
      techTags: "",
      kindTags:"",
      title : "",
      subject : "",
      content : "",
      limit : 0,
      start: "",
      end: "",
      deposit : 0,
      needmoney : 0,
    }
  },
  mounted() {
    window.scrollTo(0,0)
  },
  methods: {
    setToken () {
      const token = localStorage.getItem('jwt')
      const config = {
        headers: {
          Authorization : `Token ${token}`,
        }
      }
      return config
    },
    studyCreate () {
      const config = this.setToken()
      const data =
      {
        'title': this.title,
        'tech_tags': this.techTags,
        'kind_tags': this.kindTags,
        'subject': this.subject,
        'content': this.content,
        'member_limit': parseInt(this.limit),
        'deposit': parseInt(this.deposit),
        'needmoney' : parseInt(this.needmoney),
        'start': this.start,
        'end': this.end,
        "study_image": "string",
      }
      axios.post("https://k4b205.p.ssafy.io:7799/study/", data, config)
      .then(()=>{
        this.$router.push({ name:'MyPage'})
        // console.log(res.data)
      }).catch((err)=>{
        console.error(err);
      })
    },
    locationBack(){
      localStorage.removeItem('studyId')
      history.go(-1);
    },
  },
}
</script>

<style scoped>
</style>