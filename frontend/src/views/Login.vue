<template>
  <div class="container">
    <div class="box">
      <h1 class="backToHome" 
      @click="$router.push('/')"
      >
        로그인
      </h1>
      <div class="login-form">
        <div class="field">
          <input
            v-model="member.username"
            id="ID"
            type="text"
            placeholder="ID"
          />
          <label for="ID">Email</label>
          
        </div>
        <div class="field">
          <input 
          v-model="member.password"
          id="password"
          type="password" 
          placeholder="password" 
          
          />
          <label for="password">Password</label>
          
        </div>
        <button 
        @click="login" class="login-button" title="login">
          Login
        </button>
        <div>
          <p>
        Don't have an account?
        <router-link :to="{ name: 'Signup'}">Sign Up</router-link
        >
      </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'



export default {
  name:'login',

  data: () => {
    return {
      member: {
        username:"",
        password:"",
      },
    };
  },
  mounted() {
    window.scrollTo(0,0)
  },
  methods: {
    login: function () {
      axios.post('https://k4b205.p.ssafy.io:7799/user/login/',this.member)
      .then((res) => {
        localStorage.setItem('jwt',res.data.token)
        localStorage.setItem('user_id',res.data.user.id)
        localStorage.setItem('username',res.data.user.username)
        localStorage.setItem('email', res.data.user.email)
        alert('로그인성공')
        this.$router.push({name: 'Main'})
        location.reload()
      }).catch(()=>{
        alert('아이디 또는 비밀번호를 확인하여 주세요.')
        this.member.password = ""
      })
    },
  

  },
  
  computed: {
    
  },
};
</script>
<style scoped>
	@import url('https://fonts.googleapis.com/css2?family=Gugi&display=swap');


.container {
  height: 68vh;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin-top:1rem;
  font-size: 14px;
}

.container .box {
  max-width: 400px;
  max-height: 400px;
  width: 100%;
  /* height: 50%; */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #ffff;
  border: 1px solid #e6e6e6;
  border-radius: 1px;
  margin: 0 0 10px;
  flex-grow: 1;
}
.container .box2 { 
  max-width: 350px;
  width: 100%;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #ffff;
  border: 1px solid #e6e6e6;
  border-radius: 1px;
  flex-grow: 1;
}

.heading {
  margin: 22px auto 12px;
  background-image: url("https://www.instagram.com/static/bundles/es6/sprite_core_b20f2a3cd7e4.png/b20f2a3cd7e4.png");
  background-position: -98px 0;
  height: 51px;
  width: 177px;
  overflow: hidden;
}

.field {
  margin: 20px 0;
  position: relative;
  font-size: 14px;
  width: 100%;
  text-overflow: ellipsis;
}

input {
  padding: 9px 0px 7px 9px;
  font-size: 12px;
  width: 16rem;
  height: 3em;
  outline: none;
  background: #fafafa;
  border-radius: 3px;
  border: 1px solid #efefef;
}

/* label intial position*/

label {
  position: absolute;
  pointer-events: none;
  left: 10px;
  padding-bottom: 15px;
  transform: translateY(10px);
  line-height: 6px;
  transition: all ease-out 0.1s;
  font-size: 14px;
  color: #999;
  padding-top: 6px;
}

/* hiding placeholder in all browsers */

input::placeholder {
  visibility: hidden;
}

/* hiding  placeholder in mozilla */
.login-form ::-moz-placeholder {
  color: transparent;
}

/* label final position */
input:not(:placeholder-shown) + label {
  transform: translateY(0);
  font-size: 11px;
}

/* input padding increases if placeholder is not shown */
input:not(:placeholder-shown) {
  padding-top: 14px;
  padding-bottom: 2px;
}

.login-button {
  text-align: center;
  width: 100%;
  padding: 0.5rem;
  border: 1px solid transparent;
  background-color: #000000;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.separator {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  margin-top: 6px;
}

.separator .line {
  height: 1px;
  width: 40%;
  background-color: #dbdbdb;
}

.other {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.fb-login-btn {
  margin: 1rem;
  border: 0;
  cursor: pointer;
  font-size: 14px;
  color: #385185;
  font-weight: 600;
  background: transparent;
}

.fb-icon {
  color: #385185;
  font-size: 1rem;
  padding-right: 1px;
}

.forgot-password {
  font-size: 11px;
  color: #003569;
}

.backToHome:hover {
  color:rgb(105, 104, 104);
  cursor: pointer;
}

</style>
