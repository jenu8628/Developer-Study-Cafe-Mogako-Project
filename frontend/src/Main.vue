<template>

<div>

<!-- 로그인 했을 때 -->
  <div v-if="login">
    <div class="main-login-section1">
      <div class="main-login-section1-font">{{ nickname }}님 안녕하세요!<br>오늘도 내일도 모가코!</div>
      <img class="main-login-section1-mogako" src="@/assets/mogako.jpg">
    </div>
    <div class="main-login-section2">
      <div class="main-login-section2-font">
        진행중인 스터디🔥
      </div>
      <carousel v-if="timing" :autoplay="false" :nav="false" :dots="false" :items="itemNumber" class="main-login-section2-carousel">
        <div v-for="(item, index) in items" :key="index" @click="getStudyDetail(index, 1)" class="main-square cursor">
          <div class="main-square-img" :style="'backgroundImage: url(' + item.imgUrl + ')'">
             {{index+1}}
          </div>
          <div class="main-square-info">

          {{ item.tech_tags }}<br>
          {{ item.title }} <br>
          모집인원 : {{ item.apply_numbers }} / {{ item.member_limit }}
          </div>
        </div>
      </carousel>
    </div>
    <div class="main-login-section3">
      <div class="main-login-section2-font">
        진행중인 1:1 코칭🔥
      </div>
      <carousel v-if="timing2" :autoplay="false" :nav="true" :dots="false" :items="itemNumber" class="main-login-section2-carousel">
        <div v-for="(coaching, index) in coachings" :key="index" @click="getStudyDetail(index, 2)" class="main-square cursor">
          <div class="main-square-img" :style="'backgroundImage: url(' + coaching.imgUrl + ')'">
          {{index+1}}
          </div>
          <div class="main-square-info">
          {{ coaching.tech_tags }}<br>
          {{ coaching.title }} <br>
          모집인원: {{ coaching.apply_numbers }} / {{ coaching.member_limit }} <br>
          </div>
        </div>
      </carousel>

    </div>
    <div class="main-login-section4">
      <div class="main-login-section2-font">
        진행중인 프로젝트🔥
      </div>
      <carousel v-if="timing3" :autoplay="false" :nav="true" :dots="false" :items="itemNumber" class="main-login-section2-carousel">
        <div v-for="(project, index) in projects" :key="index" @click="getStudyDetail(index, 3)" class="main-square cursor">
          <div class="main-square-img" :style="'backgroundImage: url(' + project.imgUrl + ')'">
             {{index+1}}
          </div>
          <div class="main-square-info">

          {{ project.tech_tags }}<br>
          {{ project.title }} <br>
          모집인원 : {{ project.apply_numbers }} / {{ project.member_limit }}
          </div>
        </div>
      </carousel>

    </div>
  </div>

  <!-- 로그인 X -->
  <div class="main-all" v-else>
    <div class="main-section1">
      <div class="main-section1-description">
        <p class="main-smallfont">코딩 스터디 찾을 땐?</p>
        <span class="main-bigfont">모</span>
        <span class="main-smallfont">여서</span>
        <br>
        <span class="main-bigfont">가</span>
        <span class="main-smallfont">치</span>
        <br>
        <span class="main-bigfont">코</span>
        <span class="main-smallfont">딩</span>
      </div>
      <img class="main-section1-mogako" src="@/assets/mogako.jpg">
    </div>

    <!-- <div class="main-section2">

    </div>

    <div class="main-section3">

    </div>

    <div class="main-section4">

    </div> -->
  </div>

</div>
</template>

<script>
import carousel from 'vue-owl-carousel'
import axios from 'axios'

export default {
  components: {carousel},
  data() {
    return {
      timing: false,
      timing2: false,
      timing3: false,
      login : false,
      items : [],
      coachings : [],
      projects : [],
      nickname : localStorage.getItem('username'),
      itemNumber: 5,
      basickImage : "",

    }
  },
  methods:{
    getStudies () {
      axios.get('https://k4b205.p.ssafy.io:7799/study/')
      .then((res)=>{
        const userId = parseInt(localStorage.getItem('user_id'))
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].kind_tags === '스터디' && res.data[i].member_limit > res.data[i].apply_numbers) {
            const applied = res.data[i].members.includes(userId) 
            if (!res.data[i].confirmed && !applied && res.data[i] !== userId) {

              axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data[i].master}/`)
              .then((response)=>{
                if (!response.data.img_url) {
                  const imgUrl = this.basickImage
                  res.data[i].imgUrl = imgUrl
                } else {
                  res.data[i].imgUrl = response.data.img_url
                }
              this.timing = false
              this.items.push(res.data[i])
              })
            }
          }
          if (this.items.length === 10) {
            break
          }
        }
        setTimeout(()=>{
          this.timing = true
        },1000)
      })
    },
    getCoachings () {
      axios.get('https://k4b205.p.ssafy.io:7799/study/')
      .then((res) => {
        const userId = parseInt(localStorage.getItem('user_id'))
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].kind_tags === '1:1 코칭' && res.data[i].member_limit > res.data[i].apply_numbers) {
            const applied = res.data[i].members.includes(userId)
            if (!res.data[i].confirmed && !applied && res.data[i] !== userId) {
              axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data[i].master}/`)
              .then((response)=>{
                if (!response.data.img_url) {
                  const imgUrl = this.basickImage
                  res.data[i].imgUrl = imgUrl
                } else {
                  res.data[i].imgUrl = response.data.img_url
                }
              this.timing2 = false
              this.coachings.push(res.data[i])
              })
            }
          }
          if (this.coachings.length === 10) {
            break
          }
        }
        setTimeout(()=>{
          this.timing2 = true
        },1000)
      })
    },
    getProjects () {
      axios.get('https://k4b205.p.ssafy.io:7799/study/')
      .then((res) => {
        const userId = parseInt(localStorage.getItem('user_id'))
        for (let i = 0; i < res.data.length; i++) {
          if (res.data[i].kind_tags === '프로젝트' && res.data[i].member_limit > res.data[i].apply_numbers) {
            const applied = res.data[i].members.includes(userId)
            if (!res.data[i].confirmed && !applied && res.data[i] !== userId) {

              axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data[i].master}/`)
              .then((response)=>{
                if (!response.data.img_url) {
                  const imgUrl = this.basickImage
                  res.data[i].imgUrl = imgUrl
                } else {
                  res.data[i].imgUrl = response.data.img_url
                }
              this.timing3 = false
              this.projects.push(res.data[i])
              })
            }
          }
          if (this.projects.length === 10) {
            break
          }
        }
        setTimeout(()=>{
          this.timing3 = true
        },1000)
      })
    },
    getStudyDetail(e, number) {
      if (number === 1) {
        this.$router.push({
          name: "StudyDetail",
          query: {
            title : this.items[e].id
          }
        })
      }
      else if (number === 2) {
        this.$router.push({
          name: "StudyDetail",
          query: {
            title : this.coachings[e].id
          }
        })
      }
      else {
        this.$router.push({
          name: "StudyDetail",
          query: {
            title : this.projects[e].id
          }
        })
      }
    },
    carouselItem () {
      const wid = window.innerWidth
      if (wid > 1100) {
        if (this.itemNumber !== 5){
          this.timing = false
          this.timing2 = false
          this.timing3 = false
          this.itemNumber = 5
          setTimeout(() => {
            this.timing = true
            this.timing2 = true
            this.timing3 = true
          }, 100);
        }
      }
      if (wid < 1100 && wid > 900) {
        if (this.itemNumber !== 4){
          this.timing = false
          this.timing2 = false
          this.timing3 = false
          this.itemNumber = 4
          setTimeout(() => {
            this.timing = true
            this.timing2 = true
            this.timing3 = true
          }, 100);
        }
      } else if (wid < 900 && wid > 700) {
        if (this.itemNumber !== 3){
          this.timing = false
          this.timing2 = false
          this.timing3 = false
          this.itemNumber = 3
          setTimeout(() => {
            this.timing = true
            this.timing2 = true
            this.timing3 = true
          }, 100);
        }
      } else if (wid < 700 && wid > 500) {
        if (this.itemNumber !== 2){
          this.timing = false
          this.timing2 = false
          this.timing3 = false
          this.itemNumber = 2
          setTimeout(() => {
            this.timing = true
            this.timing2 = true
            this.timing3 = true
          }, 100);
        }
      } else if (wid < 500) {
        if (this.itemNumber !== 1){
          this.timing = false
          this.timing2 = false
          this.timing3 = false
          this.itemNumber = 1
          setTimeout(() => {
            this.timing = true
            this.timing2 = true
            this.timing3 = true
            // console.log(this.timing3)
          }, 100);
        }
      }
    },
    getBasickImage () {
      axios.get('https://k4b205.p.ssafy.io:7799/image/upload/')
      .then((res)=>{
        this.basickImage = res.data[0].uploaded_image
      })
    },
  },
  created(){
    this.getBasickImage()
    window.addEventListener('resize', ()=>{
      this.carouselItem()
    })
  },

  mounted() {
    window.scrollTo(0,0)
    const token = localStorage.getItem('jwt');
    if(token) {
      this.login = true
    }
    this.getStudies()
    this.getCoachings()
    this.getProjects()
    
  },
}
</script>

<style scoped>


.main-section1 {
  height: 80vh;
  display: flex;
  justify-content : space-between;
}

.main-section1-description{
  margin-left: 200px;
  margin-top: 130px;
}

.main-section1-mogako {
  width: 100vh;
  margin-right: 90px;
  margin-top: 50px;
  
  /* margin-left: 500px;
  margin-top: 75px; */
}

.main-login-section1-mogako {
  width: 70vh;
  /* margin-left: 400px; */
  margin-top: 40px;
}

.main-section2 {
  height: 80vh;
  background-color: #e8f1ff;
  /* border: solid 1px red; */
}

.main-section3 {
  height: 80vh;
}

.main-section4 {
  height: 80vh;
  background-color: #e8f1ff;
  /* border: solid 1px red; */
}

.main-bigfont {
  font-size: 40px;
}

.main-smallfont {
  font-size: 20px;
}

.main-square {
  /* border-radius: 15px; */
  display: flex;
  height: 300px;
  width: 200px;
  margin: 30px 0;
  box-shadow: 8px 8px 10px rgba(0, 0, 0, 0.55);
  background-color: white;
  transition: ease 0.5s;
  flex-flow: column;
}

.main-login-section1 {
  display: flex;
  height: 60vh;
  width: 100%;
  justify-content: center;
}

.main-login-section1-font {
  font-size: 20px;
  text-align: center;
  display: flex;
  align-items: center;
}

.main-login-section2 {
  /* border: solid 1px red; */
  /* background-color: #ebf6ff; */
}

.main-login-section2-font {
  margin-left: 20px;
  font-size: 25px;
}



.main-login-section2-carousel {
  height: 400px;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
}

.main-square-img {
  display: flex;
  height: 200px;
  width: 100%;
  /* background-color: greenyellow; */
  transition: ease 0.5s;
  background-size: cover;
  /* border-radius: 5%; */
}
.main-square-info {
  margin-top: 10px;
  display: flex;
  height: 100px;
  width: 100%;
  justify-content: center;
  ;
  background-color: white;
  transition: ease 0.5s;
}

.main-login-section3 {
  /* border: solid 1px red; */
  /* background-color: #f2fff6; */
}

.main-login-section4 {
  /* background-color: #fffafe; */
  overflow: hidden;
}

.cursor:hover {
  cursor: pointer;
}

.main-square:hover{
   transform: scale(1.05);
}

</style>