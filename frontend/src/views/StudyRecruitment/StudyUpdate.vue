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
      techTags: this.$route.query.tech_tags,
      title : this.$route.query.title,
      subject : this.$route.query.subject,
      content : this.$route.query.content,
      limit : this.$route.query.member_limit,
      kindTags : this.$route.query.kind_tags,
      needmoney : this.$route.query.needmoney,
    }
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
        'apply_numbers' : parseInt(this.$route.query.apply_numbers),
        'master' : parseInt(this.$route.query.master)
      }
      const studyId = parseInt(this.$route.query.id)
      axios.put(`https://k4b205.p.ssafy.io:7799/study/${studyId}/`, data, config)
      .then((res)=>{
        if (res.data === "wrong number") {
          alert('제한인원을 신청인원보다 늘려주세요!')
        } else {
          localStorage.setItem('studyId', studyId)
          this.$router.push({name:"MyPage"})
        }
      }).catch((err)=>{
        console.error(err);
      })
    },
    locationBack(){
      history.go(-1);
    },
  },
  mounted() {
    window.scrollTo(0,0)
    localStorage.removeItem('studyId')
  },
}
</script>

<style scoped>
.disable {
  color: rgb(172, 170, 170);
}
</style>