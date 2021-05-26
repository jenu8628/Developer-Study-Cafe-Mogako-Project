<template>
  <div class="FreeStudyList-container">
    <div class="FreeStudyList-title">
      <div 
        class="FreeStudyList-study"
      >
        {{title}}
      </div>
      <i class="FreeStudyList-create cursor fas fa-plus-square" @click="$router.push({name:'StudyCreate'})"></i>
    </div>
    <div class="FreeStudyList-box">
      <div @click="getStudyDetail(idx)" class="FreeStudyList-list" v-for="(list, idx) in studyList" :key="idx">
          <div class="list-front">
            <div class="list-content">
              <div class="list-content-margin">{{list.subject}}</div>
              <div class="">#{{list.tech_tags}}</div>
              <div class=""> {{list.apply_numbers}} / {{list.member_limit}} </div>
              <div class="">{{list.needmoney}}원</div>
              </div>

            <!-- <img class="img-box" :src="list.profile_image" alt=""> -->
            <div 
              class="img-box"
              :style="'backgroundImage: url(' + list.profile_image + ')'">
            </div>
          </div>
      </div>
    </div>
    
    <infinite-loading class="loading" spinner="default" @infinite="infiniteHandler">
      <div slot="no-more"></div>
      <div slot="no-results"></div>
    </infinite-loading>
  </div>
</template>

<script>
import axios from 'axios';
import '@/assets/css/list.css'

export default {
  data() {
    return {
      title: this.$route.query.title,
      studyList:[],
      discrime:false,
      limit:0,
      allList : [],
      basickImage : ""
    }
  },
  created() {
    
    },
  mounted() {
    window.scrollTo(0,0)
    this.getBasickImage()
    this.getStudy();
  },
  methods: {
    getStudy () {
      const userId = parseInt(localStorage.getItem('user_id'))
      axios.get('https://k4b205.p.ssafy.io:7799/study/')
      .then((res)=> {
        const data = res.data.filter((data)=>{
          return data.kind_tags.includes(this.$route.query.title)
        })
        for (let i = 0; i<data.length; i++) {
          if (data[i].member_limit > data[i].apply_numbers) {
            const applied = data[i].members.includes(userId)
            if (!data[i].confirmed && !applied && data[i].master !== userId) {
              axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${data[i].master}/`)
              .then((response)=>{
                if (!data[i]['profile_image']) {
                  data[i]['profile_image'] = this.basickImage
                } else {
                  data[i]['profile_image'] = "https://k4b205.p.ssafy.io:7799"+response.data.profile_image
                }
              })
              this.allList.push(data[i])
            }
          }
        }
      })
    },
    getBasickImage () {
      axios.get('https://k4b205.p.ssafy.io:7799/image/upload/')
      .then((res)=>{
        this.basickImage = res.data[0].uploaded_image
      })
    },
    infiniteHandler($state) {
      if (this.limit > 0) {
        setTimeout(()=>{
          for (let i=this.limit; i<this.limit+16; i++){
            if (i > this.allList.length - 1 ) {
              $state.complete();
            } else{
              this.studyList.push(this.allList[i])
            }
          }
          this.limit += 4
          
          $state.loaded();
        },1500)
      } else {
        setTimeout(() => {
          for (let i =0; i< 8; i++){
            if (i > this.allList.length - 1 ) {
              $state.complete();
            } else{
              this.studyList.push(this.allList[i])
              this.limit += 1
            }
          }
          $state.loaded();
        }, 1000);
      }
    },
    getStudyDetail(e) {
      this.$router.push({
        name: "StudyDetail",
        query: {
          title: this.allList[e].id
        }
      })
    },
  },
}
</script>

<style scoped>
</style>