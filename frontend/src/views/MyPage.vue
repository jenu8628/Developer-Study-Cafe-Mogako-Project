<template>
  <div class="mypage-container">
		<div class="profile">
      <div class="profile-image">
        <i v-if="updateProfile" @click="profileUpdate(0)" class="updateProfile cursor fas fa-pencil-alt"></i>
        <div v-else @click="profileUpdate(1)" class="updateProfile cursor a">
          수정 완료
        </div>
        <i ></i>
        <div class="avatar-upload">
            <div class="avatar-edit">
              <input
                type="file"
                id="imageUpload"
                @change="onImages"
              />
              <label for="imageUpload" v-if="!updateProfile">
                <i class="fas fa-pencil-alt"></i>
              </label>
            </div>
            <div class="avatar-preview" >
              <div id="prev-img" class="prev-img"></div>
            </div>
          </div>
      </div>
      <div class="userinfo">
        <div>{{user.username}}</div>
        <div> {{user.email}}</div>
        <div>{{user.money}} 원</div>
        <div class="edit-message">
          <div v-if="updateProfile">
            <div v-if="messageContent">소개글을 입력하세요.</div>
            <div v-else> {{user.message}} </div>
          </div>
          <div v-else>
            <input
            class="message-input"
            type="text" 
            v-model="message"
            id="message-upload"
            placeholder="소개글을 입력하세요">
          </div>
        </div>
      </div>
    </div>

    <div class="study-list">
      <div class= "study-list-font">승인해야 할 스터디🔥</div>
      <carousel v-if ="timing" :autoplay="false" :nav="true" :dots="false" :items="itemNumber" class="study-list-carousel">
        <div v-for="(item, index) in studyMaster" :key="index" @click="getStudyDetail(index, 1)" class="study-square cursor">
          <div class="study-square-img" :style="'backgroundImage: url(' + item.imgUrl + ')'">{{index+1}}</div>
          <div class="study-square-info">
          {{ item.title }} <br>
          {{ item.tech_tags }} <br>
          모집 인원: {{ item.apply_numbers }} / {{ item.member_limit }} <br>
          </div>
        </div>
      </carousel>
    </div>

    <div class="study-list2">
      <div class="study-list2-font">내가 지원한 스터디🔥</div>
      <carousel v-if ="timing" :autoplay="false" :nav="true" :dots="false" :items="itemNumber" class="study-list2-carousel">
        <div v-for="(item2, index) in study" :key="index" @click="getStudyDetail(index, 2)" class="study-square cursor">
          <div class="study-square-img " :style="'backgroundImage: url(' + item2.imgUrl + ')'">{{index+1}}</div>
          <div class="study-square-info">
          {{ item2.title }} <br>
          {{item2.tech_tags}}<br>
          모집인원: {{ item2.apply_numbers }}/ {{ item2.member_limit }}
          </div>
        </div>
      </carousel>
    </div>

    <div class="study-list3">
      <div class="study-list3-font">진행중인 스터디🔥</div>
      <carousel v-if ="timing" :autoplay="false" :nav="true" :dots="false" :items="itemNumber" class="study-list3-carousel">
        <div v-for="(item3, index) in studying" :key="index" @click="getStudyDetail(index, 3)" class="study-square cursor">
          <div class="study-square-img" :style="'backgroundImage: url(' + item3.imgUrl + ')'">{{index+1}}</div>
          <div class="study-square-info">
          {{ item3.title }} <br>
          {{item3.tech_tags}}<br>
          모집인원: {{ item3.apply_numbers }}/ {{ item3.member_limit }}
          </div>
        </div>
      </carousel>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import carousel from 'vue-owl-carousel'


export default {
  components: {carousel},
  data() {
    return {
      img:null, //이미지
      username:"",
      email:"",
      profile_image:"",
      message:"",
      user:"",
      studyMaster:[],
      study:[],
      studying:[],
      itemNumber: 5,
      timing : false,
      messageContent : false,
      updateProfile : true,
      basickImage : "",
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
    getProfile(){
      const userId = parseInt(localStorage.getItem('user_id'))
      axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${userId}/`)
      .then((res)=>{
        this.user = res.data
        this.message = this.user.message
        const prevImg = document.querySelector("#prev-img");
        prevImg.style.backgroundImage = "url(" + `${this.user.img_url}` + ")";
        if (this.user.message === "") {
          this.messageContent = true
        }
        
        for (let i = 0; i<res.data.study.length; i++){
          if (res.data.study[i].master === userId && res.data.study[i].confirmed === false) {
            axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data.study[i].master}/`)
            .then((response)=>{
              if (!response.data.img_url) {
                const imgUrl = this.basickImage
                res.data.study[i].imgUrl = imgUrl
              } else {
                res.data.study[i].imgUrl = response.data.img_url
              }
              this.studyMaster.push(res.data.study[i])
              this.timing = false
            })
            // 내가 만든 스터디
          } else if (res.data.study[i].master !== userId && res.data.study[i].confirmed === false){
            axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data.study[i].master}/`)
            .then((response)=>{
              if (!response.data.img_url) {
                const imgUrl = this.basickImage
                res.data.study[i].imgUrl = imgUrl
              } else {
                res.data.study[i].imgUrl = response.data.img_url
              }
              this.study.push(res.data.study[i])
              this.timing = false
            })
            // 내가 지원한 스터디
          } else if (res.data.study[i].confirmed === true) {
            axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${res.data.study[i].master}/`)
            .then((response)=>{
              if (!response.data.img_url) {
                const imgUrl = this.basickImage
                res.data.study[i].imgUrl = imgUrl
              } else {
                res.data.study[i].imgUrl = response.data.img_url
              }
              this.studying.push(res.data.study[i])
              this.timing = false
            })
          }
        }
        // console.log(this.studying)
        setTimeout(() => {
          
          this.timing = true
        }, 1000);
        
      })
    },
    onImages(e) {
      this.img = e.target.files[0];
      this.previewImg = URL.createObjectURL(this.img);
      const prevImg = document.querySelector("#prev-img");
      prevImg.style.backgroundImage = "url(" + `${this.previewImg}` + ")";
    },
    getStudyDetail(e, number) {
      if (number === 1) {
        this.$router.push({
          name: "StudyDetail",
          query: {
            title:this.studyMaster[e].id
          }
        })
      }
      else if (number === 2) {
        
        this.$router.push({
          name: "StudyDetail",
          query: {
            title:this.study[e].id
          }
        })
      }
      else {
        this.$router.push({
          name: "BoardList",
          query: {
            title:this.studying[e].id
          }
        })
      }
      
    },
    carouselItem () {
      const wid = window.innerWidth
      if (wid > 1100) {
        if (this.itemNumber !== 5){
          this.timing = false
          this.itemNumber = 5
          setTimeout(() => {
            this.timing = true
          }, 100);
        }
      }
      if (wid < 1100 && wid > 900) {
        if (this.itemNumber !== 4){
          this.timing = false
          this.itemNumber = 4
          setTimeout(() => {
            this.timing = true
          }, 100);
        }
      } else if (wid < 900 && wid > 700) {
        if (this.itemNumber !== 3){
          this.timing = false
          this.itemNumber = 3
          setTimeout(() => {
            this.timing = true
          }, 100);
        }
      } else if (wid < 700 && wid > 500) {
        if (this.itemNumber !== 2){
          this.timing = false
          this.itemNumber = 2
          setTimeout(() => {
            this.timing = true
          }, 100);
        }
      } else if (wid < 500) {
        if (this.itemNumber !== 1){
          this.timing = false
          this.itemNumber = 1
          setTimeout(() => {
            this.timing = true
          }, 100);
        }
      }
    },
    profileUpdate (e){
      if(e === 1) {
        if (this.img === null) {
          alert('프로필 이미지를 수정하세요!')
        } else if (this.message === ""){
          alert('메세지를 입력하세요!')
        } else {
          const config = this.setToken()
          const userId = parseInt(localStorage.getItem('user_id'))
          var formData = new FormData();
          formData.append('profile_image', this.img)
          formData.append('message', this.message)
          formData.append('user', userId)
          axios.put(`https://k4b205.p.ssafy.io:7799/user/profile/${userId}/`,formData, config)
          .then(()=>{
            alert('수정 완료')
            location.reload()
          })
        }
      } else {
        this.updateProfile = !this.updateProfile
      }
    },
    getBasickImage () {
      axios.get('https://k4b205.p.ssafy.io:7799/image/upload/')
      .then((res)=>{
        this.basickImage = res.data[0].uploaded_image
      })
    },
  },
  mounted(){
    this.getBasickImage()
    this.getProfile()
    this.carouselItem()
    window.scrollTo(0,0)
  },
  created() {
    window.addEventListener('resize', ()=>{
      this.carouselItem()
    })
  },
}

</script>

<style scoped>


.mypage-container {
  overflow: hidden;
  display: flex;
  width: 100%;
  flex-flow: column;
  justify-content: center;
  position: relative;
}
.mypage-container .updateProfile{
  font-size: 1.5rem;
  position: absolute;
  top:20px;
  right: 10vw;
  /* z-index: 10; */
}
.mypage-container .cursor:hover{
  cursor: pointer;
}
.mypage-container .cursor.a{
  transition: 1s ease;
}
.mypage-container .cursor.a:hover{
  transform: scale(1.1);
}

.mypage-container .profile {
  border-bottom: 1px solid black;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.profile-image {
  width: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.userinfo {
  width: 100%;
  font-size:1.5rem;
  display: flex;
  flex-flow: column;
  align-items: center;
}
.userinfo > div {
  padding: 10px;
}

.userinfo .message-input {
  font-size: 1rem;
  border-top: none;
  border-left: none;
  border-right: none;
  transition: 0.5s ease;
}
.userinfo .message-input:focus{
  outline: none;
  border-bottom: 2px solid #aac3eb;
  box-shadow: 5px 5px 5px 1px #c6d6f079;
}

/* 내가 만든 스터디 */
.mypage-container .study-list {
  
  height: 60vh;
  width: 100%;
  /* border-bottom: 1px solid black; */
  flex-flow: column;
  

}
.mypage-container .study-list .study-list-font {
  margin-left: 20px;
  
  margin-top: 10px;
  font-size: 25px;

}
.mypage-container .study-list .study-list-carousel {
  height: 400px;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
  
  
}
.mypage-container .study-list .study-square {
  display: flex;
  height: 300px;
  width: 200px;
  margin: 30px 0;
  box-shadow: 8px 8px 10px rgba(0, 0, 0, 0.55);
  background-color: white;
  transition: ease 0.5s;
  flex-flow: column;  
  
}

.mypage-container .study-list .study-square .study-square-img {
  display: flex;
  height: 200px;
  width: 100%;
  background-size: cover;
  transition: ease 0.5s;
  border-radius: 5%;
}
.mypage-container .study-list .study-square .study-square-info {
  margin-top: 10px;
  display: flex;
  height: 100px;
  width: 100%;
  justify-content: center;
  background-color: white;
  transition: ease 0.5s;
}

.mypage-container .study-list .study-square:hover {
  transform: scale(1.05);
}
/* 내가 지원한 스터디 */
.mypage-container .study-list2 {

  height: 60vh;
  width: 100%;
  flex-flow: column;
  /* border-bottom: 1px solid black; */
  

}
.mypage-container .study-list2 .study-list2-font {
  margin-left: 20px;
  margin-top: 10px;
  font-size: 25px;

}
.mypage-container .study-list2 .study-list2-carousel {
  height: 400px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
  
  
}
.mypage-container .study-list2 .study-square {
  display: flex;
  height: 300px;
  width: 200px;
  margin: 30px 0;
  box-shadow: 8px 8px 10px rgba(0, 0, 0, 0.55);
  background-color: white;
  transition: ease 0.5s;
  flex-flow: column;
}

.mypage-container .study-list2 .study-square .study-square-img {
  display: flex;
  height: 200px;
  width: 100%;
  /* background-color: greenyellow; */
  background-size: cover;
  transition: ease 0.5s;
  border-radius: 5%;
}
.mypage-container .study-list2 .study-square .study-square-info {
  display: flex;
  margin-top: 10px;
  height: 100px;
  width: 100%;
  justify-content: center;
  background-color: white;
  transition: ease 0.5s;
}


.mypage-container .study-list2 .study-square:hover {
  transform: scale(1.05);
}
/* 진행중인스터디 */
.mypage-container .study-list3 {

  height: 60vh;
  width: 100%;
  flex-flow: column;
  /* border-bottom: 1px solid black; */
  

}
.mypage-container .study-list3 .study-list3-font {
  margin-left: 20px;
  margin-top: 10px;
  font-size: 25px;

}
.mypage-container .study-list3 .study-list3-carousel {
  height: 400px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 20px;
  
  
}
.mypage-container .study-list3 .study-square {
  display: flex;
  height: 300px;
  width: 200px;
  margin: 30px 0;
  box-shadow: 8px 8px 10px rgba(0, 0, 0, 0.55);
  background-color: white;
  transition: ease 0.5s;
  flex-flow: column;
}

.mypage-container .study-list3 .study-square .study-square-img {
  display: flex;
  height: 200px;
  width: 100%;
  background-size: cover;
  transition: ease 0.5s;
  border-radius: 5%;
}
.mypage-container .study-list3 .study-square .study-square-info {
  display: flex;
  margin-top: 10px;
  height: 100px;
  width: 100%;
  justify-content: center;
  background-color: white;
  transition: ease 0.5s;
}


.mypage-container .study-list3 .study-square:hover {
  transform: scale(1.05);
}





.avatar-upload {
  display:flex;
  width: 192px;
  height: 192px;
  margin:5%;
}

.avatar-upload .avatar-edit {
  position: relative;
  z-index: 1;
  order: 1;
}
.avatar-upload .avatar-edit input {
  display: none;
}
.avatar-upload .avatar-edit label {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  right: 0;
  z-index: 5;
  width: 34px;
  height: 34px;
  margin-bottom: 0;
  border-radius: 100%;
  background: #FFFFFF;
  border: 1px solid transparent;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  cursor: pointer;
  font-weight: normal;
  transition: all .2s ease-in-out;
}
.avatar-upload .avatar-edit label:after{
  color: #757575;
  top: 10px;
  left: 0;
  right: 0;
  text-align: center;
  margin: auto;
}
.avatar-upload .avatar-preview {
  width: 192px;
  height: 192px;
  border-radius: 100%;
  border: 1px solid #F8F8F8;
  box-shadow: 0px 0px 5px 5px rgba(0, 0, 0, 0.1);
}
.avatar-upload .avatar-preview > div {
  width: 100%;
  height: 100%;
  border-radius: 100%;
  background-size: cover;
  background-position: center;
}





</style>