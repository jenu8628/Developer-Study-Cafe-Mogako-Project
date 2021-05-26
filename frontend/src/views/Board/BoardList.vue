<template>
  <div class="boardlist-container">
    <div class="boardlist-box">
      <div class="boardlist-member">
        <div class="btn-group">
          <div @click="ban(0)" class="cursor btn" v-if="master">강퇴하기</div>
          <div @click="giveUp" class="cursor btn" v-else>포기하기</div>
          <div @click="expire" class="cursor btn" v-if="master">정산하기</div>
        </div>
        <div class="a">멤버</div>

        <div class="member-profile">
          <div @click="banPick(profile.id)" v-for="profile, idx in profiles" :key="idx">
            <div class="profile" 
            :style="'backgroundImage: url(' + profile.image + ')'">
            </div>
            <div class="profile-name">{{profile.username}}</div>
          </div>
        </div>

        <div class="a"> 목표 과제 </div>
        <div class="subject">{{subject}}</div>
        
      </div>
      <i class="cursor fas fa-plus-square" @click="createBoard"></i>
      <div class="boardlist-list" v-for="(article, index) in articles" :key="index">
        <div @click="goDetail(article.id)" class="list-title cursor">{{article.title}}</div>
        <div class="list-content">{{article.content}}</div>
        <div class="small-box">
          <div class="set">{{article.writer.username}} / </div>
          <div class="set">{{article.created_at[0]}} {{article.created_at[1]}} /</div>
          <div class="view set">조회 수 
            <span class="span">
              {{article.viewed_num}}
            </span>
          </div>
        </div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      articles : [],
      studyId : this.$route.query.title,
      boardId : null,
      profiles: [],
      subject : "",
      master : false,
      masterId: "",
      giveUpModal : false,
      banPickMember : "",
      banActive : false,
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
    getProfiles () {
      const studyId = parseInt(this.studyId)
      const config = this.setToken()
      axios.get(`https://k4b205.p.ssafy.io:7799/study/${studyId}/`, config)
      .then((res)=>{
        this.subject = res.data.subject
        this.masterId = res.data.master
        if (res.data.master === parseInt(localStorage.getItem('user_id'))){
          this.master = true
        }
        for (let i = 0; i<res.data.members.length; i++) {
          const userId = res.data.members[i]
          axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${userId}/`)
          .then((response)=> {
            if (response.data.profile_image === "") {
              this.profiles.push({
                id : response.data.id,
                username : response.data.username,
                image : "https://k4b205.p.ssafy.io:7799/media/2021/05/17/user_2_sACiJmO.png"
              })
            } else {
              this.profiles.push({
                id : response.data.id,
                username : response.data.username,
                image : "https://k4b205.p.ssafy.io:7799"+response.data.profile_image
              })
            }
          })
        }
      })
    },
    getGroupBoard () {
      axios.get(`https://k4b205.p.ssafy.io:7799/board/board/${this.studyId}/`)
      .then((res)=>{
        this.boardId = res.data[0].board
        const config = this.setToken()
        axios.get(`https://k4b205.p.ssafy.io:7799/board/${this.boardId}/article/`, config)
        .then((response)=>{
          if (response.data.length !== 0) {
            this.articles = response.data
            for (let i = 0; i < this.articles.length; i++) {
              this.articles[i].created_at = [
                this.articles[i].created_at.substring(0,10), 
                this.articles[i].created_at.substring(11,16)
              ]
            }
          }
        })
      })
    },
    goDetail(articleId) {
      this.$router.push({
        name: "BoardDetail",
        query: {
          title : this.boardId,
          body: articleId
        }
      })
    },
    createBoard () {
      this.$router.push({
        name:'BoardCreate',
        query: {
          title : this.boardId,
          body: this.studyId
        }
      })
    },
    banPick (event) {
      this.banPickMember = event
      this.ban(1)
    },
    ban (event) {
      const profile = document.querySelector('.profile')
      if (event === 0) {
        alert('추방할 멤버를 선택하세요.')
        this.banActive = true
        if (this.banActive) {
          profile.classList.add('ban-cursor')
        }
      } else if (event === 1 && this.banActive) {
        if (parseInt(this.banPickMember) === parseInt(this.masterId)){
          alert('그룹장은 추방할 수 없습니다.')
          profile.classList.remove('ban-cursor')
        } else {
          const flag = confirm('정말로 추방하시겠습니까?')
          if (flag) {
            const config = this.setToken()
            const user = {
              "apply_user": this.banPickMember
            }
            axios.post(`https://k4b205.p.ssafy.io:7799/ban/${this.studyId}/`, user, config)
            .then(()=>{
              profile.classList.remove('ban-cursor')
              alert('추방하였습니다.')
              this.getProfiles()
            })
          } else {
            profile.classList.remove('ban-cursor')
          }
        }
      }
    },
    giveUp() {
      const flag = confirm('정말로 포기하시겠습니까?')
      const config = this.setToken()
      const user = {
        'id' : parseInt(localStorage.getItem('username')),
        'username' : localStorage.getItem('username'),
        'email' : localStorage.getItem('email'),
      }
      if (flag) {
        axios.post(`https://k4b205.p.ssafy.io:7799/giveup/${this.studyId}/`,user,config)
        .then(()=> {
          alert('포기하였습니다.')
        })
      }
      
    },
    expire() {
      const config = this.setToken()
      axios.post(`https://k4b205.p.ssafy.io:7799/expire/${this.studyId}/`,config)
      .then((res)=>{
        if (res.data[0] === "이미 정산되었습니다") {
          alert('이미 정산되었거나, 마감날짜가 아닙니다.')
        }
      })
    },
  },
  mounted() {
    window.scrollTo(0,0)
    this.getGroupBoard()
    this.getProfiles()
  },
}
</script>

<style scoped>
.boardlist-container {
  margin-top: 100px;
  width: 100%;
  min-height: 100vh;
  padding-bottom: 10vh;
  display: flex;
  justify-content: center;
}
.boardlist-container.modal {
  height: 100vh;
  overflow: hidden;
}

.giveup-modal {
  position: absolute;
  overflow: hidden;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background: rgba(0, 0, 0, .7);
  backdrop-filter: saturate(180%) blur(3px);
  z-index: 999;
}

.boardlist-container .boardlist-box {
  width: 80%;
}
.boardlist-container .boardlist-box .giveup-container{
  width: 100%;
  height: 100%;
}



.boardlist-container .boardlist-box .boardlist-member{
  width: 100%;
}
.boardlist-container .boardlist-box .boardlist-member .a{
  font-size: 2rem;
  border-bottom: 1px solid grey;
  margin-bottom: 10px;
  margin-top: 30px;
}
.boardlist-container .boardlist-box .boardlist-member .subject{
  font-size: 2rem;
  margin-bottom: 70px;
  margin-top: 30px;
}
.boardlist-container .boardlist-box .boardlist-member .btn-group{
  font-size: 1.5rem;
  width: 100%;
  display: flex;
  justify-content: space-around;
}

.boardlist-container .boardlist-box .boardlist-member .btn{
  transition: ease 1s;
}
.boardlist-container .boardlist-box .boardlist-member .btn:hover{
  transform: scale(1.1);
  transition: ease 1s;
}


.boardlist-container .boardlist-box .member-profile{
  width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.boardlist-container .boardlist-box .profile{
  width: 80px;
  height: 80px;
  display: flex;
  margin-right: 20px;
  background-size: cover;
  background-position: center;
  box-shadow: 0px 0px 5px 5px rgba(122, 122, 122, 0.596);
  border-radius: 100%;
  margin-top: 10px;
  transition: 1s ease;
}
.boardlist-container .boardlist-box .profile-name{
  margin-right: 20px;
  text-align: center;
  margin-top: 10px;
}


.boardlist-container .boardlist-box .fas{
  font-size: 3rem;
  margin-left: 100%;
  margin-bottom: 10px;
}
.boardlist-container .boardlist-box .cursor:hover {
  cursor: pointer;
}
.ban-cursor:hover {
  cursor: pointer;
  transform: scale(1.2);
}


.boardlist-container .boardlist-box .boardlist-list{
  border-bottom: 1px black solid;
  font-size: 1.5rem;
  margin-bottom: 30px;
}
.boardlist-container .boardlist-box .boardlist-list .list-title {
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  margin-bottom: 10px;
  width: 70%;
}

.boardlist-container .boardlist-box .boardlist-list .list-content {
  margin-bottom: 10px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  min-width: 300px;
  width: 70%;
}

.boardlist-container .boardlist-box .boardlist-list .small-box {
  display: flex;
  margin-bottom: 10px;
}
.boardlist-container .boardlist-box .boardlist-list .small-box .set{
  margin-right: 10px;
  font-size: 1.2rem;
  color: rgb(112, 112, 112);
}
.boardlist-container .boardlist-box .boardlist-list .small-box .view .span{
  color: rgb(255, 115, 0);
}
  



</style>