<template>
  <div id="app">
    <div class="app-container">
      <div class="app-nav">
        <router-link class="home-logo" to="/">모가코</router-link>
        <!-- <div>로그인</div> -->
        <i v-if="login" @click="menuActive" class="fas fa-bars menu-logo"></i>
        <i v-else class="fas fa-sign-in-alt menu-logo" @click="direction('Login', 2)"></i>
      </div>
      <div v-if="navMenu" class="active-menu">
        <div class="active-menu-box">
          <div class="close-menu menu-font" @click="menuActive">닫기</div>
          <div class="active-menu-Home menu-font" @click="direction('Main', 2)">홈</div>
          <div class="active-menu-free menu-font" @click="direction('스터디', 1)">스터디</div>
          <div class="active-menu-mento menu-font" @click="direction('프로젝트', 1)">프로젝트</div>
          <div class="active-menu-personal menu-font" @click="direction('1:1 코칭', 1)">1:1코칭</div>
          <div class="active-menu-mypage menu-font" @click="direction('MyPage', 2)">마이페이지</div>
          <div class="active-menu-logout menu-font" @click="logout">로그아웃</div>
        </div>
      </div>
    </div>
    <router-view/>
    <!-- <Footer/> -->
    <div class="Footer-container">
      <div class="Footer-font1">
        Mogako
      </div>
      <div class="Footer-font2">
        <a href="">Kim ByeongSu</a>
        <a href="">Nam HyunJun</a>
        <a href="">Lee HyunWoo</a>
        <a href="">Jung DaeYoung</a>
        <a href="">Choi JuA</a>
      </div>
    </div>
  </div>
</template>

<script>
// import Footer from '@/views/Footer.vue'
import axios from 'axios'

export default {
  // components:{
  //   Footer
  // },
  data () {
    return {
      navMenu : false,
      login : false,
    }
  },
  mounted() {
    const token = localStorage.getItem('jwt')
    if (token) {
      this.login = true
    }
  },
  methods: {
    menuActive () {
      this.navMenu = !this.navMenu
      if (this.navMenu){
        setTimeout(() => {
          document.querySelector('.active-menu').style.top = `${window.pageYOffset}px`
        }, 100);
        document.querySelector('body').classList.add('body-style')
      } else {
        document.querySelector('body').classList.remove('body-style')
      }
    },
    direction (event, num) {
      if (this.$route.name === event) {
        location.reload()
      } else {
        if (this.login) {
          this.menuActive()
        }
        if (num === 1) {
          this.$router.push({
            name:"StudyList",
            query: {
              title : event
            }
          })
          location.reload()
        } else {
          this.$router.push({name: event})
        }
      }
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
    logout () {
      const config = this.setToken()
      axios.get('https://k4b205.p.ssafy.io:7799/user/logout/',config)
      .then(()=>{
        this.login = false
        localStorage.clear()
        this.menuActive()
        this.$router.push({name:'Login'})
      })
    }
  },
  
}
</script>

<style>


body {
  margin:10vh 0 0 0;
}
.body-style {
  height: 100vh;
  overflow: hidden;
}
.app-container{
  overflow: hidden;
}
.app-nav {
  position: fixed;
  top: 0;
  left: 0;
  height: 10vh;
  width: 100%;
  border-bottom: 1px solid black;
  display: flex;
  align-items: center;
  background: white;
  z-index: 10;
}
.app-nav .home-logo {
  text-decoration: none;
  color: black;
}
.app-nav .menu-logo:hover,
.close-menu:hover,
.active-menu-Home:hover,
.active-menu-mypage:hover,
.active-menu-free:hover,
.active-menu-mento:hover,
.active-menu-personal:hover,
.active-menu-mypage:hover,
.active-menu-logout:hover
{
  cursor: pointer;
}
.app-nav .home-logo{
  margin-left: 5%;
  margin-right: auto;
}
.app-nav .menu-logo{
  margin-right: 5%;
  font-size: 2rem;
}


.active-menu {
  position: absolute;
  overflow: hidden;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, .7);
  backdrop-filter: saturate(180%) blur(3px);
  z-index: 999;
}
.active-menu .active-menu-box {
  position: absolute;
  /* background: #e8f1ff; */
  background: #d2d3d6;
  top: 0;
  right: 0;
  width: 30vw;
  height: 100vh;
  animation-duration: 0.3s;
  animation-name: openmenu;
}
@keyframes openmenu {
  0% {
    right: -100%;
  }
  100% {
    right: 0%;
  }
}
/* .active-menu .active-menu-box .close-menu{
  margin-top: 5%;
} */
.active-menu .active-menu-box .menu-font {
  height: 8%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.3rem;
}
.active-menu .active-menu-box .menu-font:hover{
  background:  #e8f1ff;
}

.Footer-container {
  display: flex;
  height: 20vh;
  background: #91a2a8;
  justify-content: center;

}

.Footer-font1 {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
  color: antiquewhite;
  padding-right: 100px;
}

.Footer-font2 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}

.Footer-font2 > a {
  text-decoration: none;
  color: antiquewhite;
}


@font-face {
    font-family: 'MaplestoryOTFLight';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/MaplestoryOTFLight.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
/* * {
  font-family: "MaplestoryOTFLight", serif;
} */

@font-face {
    font-family: 'SEBANG_Gothic_Bold';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2104@1.0/SEBANG_Gothic_Bold.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
* {
  font-family: "SEBANG_Gothic_Bold", serif;
}
</style>
