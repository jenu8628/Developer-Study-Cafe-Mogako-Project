<template>
  <div class="container">
    <div class="box">
      <h1 class="backToHome" 
      @click="$router.push('/')"
      >
        회원가입
      </h1>
      <form @submit.prevent="join" class="login-form">
        <div class="field">
          <input
            class="input_style"
            v-model="join.email"
            id="email"
            type="name"
            placeholder="email"
          />
          <label for="email">Email</label>
        </div>
        <div class="field">
          <input
            class="input_style"
            v-model="join.username"
            id="username"
            type="text"
            placeholder="username"
          />
          <label for="username">Username</label>
        </div>
        <div class="field">
          <input
            class="input_style"
            v-model="join.password"
            id="password"
            type="password"
            placeholder="password"
          />
          <label for="password">Password</label>
        </div>
        <div class="field">
          <input
            class="input_style"
            id="passwordconfirmation"
            type="password"
            v-model="join.passwordconfirm"
            placeholder="passwordconfirmation"
          />
          <label for="passwordconfirmation">PasswordConfirm</label>
        <div>
          <button @click="Join" class="login-button" type="submit">Signup</button>
        </div>
        </div>
      </form>
    </div>

  </div>
</template>


<script>
import axios from "axios";


export default {
  name: "Signup",
  data() {
    return {
      join: {
        username: "",
        email:"",
        password: "",
        passwordconfirm: "",
      },
    };
  },
  mounted() {

  },
  components: {},
  created() {},
  methods: {
    Join() {
    axios.post('https://k4b205.p.ssafy.io:7799/user/register/',this.join)
      .then(()=>{
        if (this.join.password !== this.join.passwordconfirm) {
          alert('비밀번호가 틀립니다.')
          this.join.password = ""
          this.join.passwordconfirm = ""
        } else {
          alert('회원가입 되었습니다.')
          this.$router.push({name: 'Login'})
        }
      })
      .catch((err)=>{
        console.log(err)
        alert('오류가 발생했습니다. 다시 입력해 주세요.')
        location.reload()
      })
    },


  },
  watch: {},

  computed: {},
};
</script>
<style scoped>


.container {
  height: 65vh;
  /* max-width: 1500px; */
  margin: 0 auto;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin-top: 3rem;
  font-size: 14px;
}

.box {
  max-width: 350px;
  max-height: 500px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-color: #ffff;
  border: 1px solid #e6e6e6;
  border-radius: 1px;
  margin: 0 0 10px;
  padding: 20px 0;
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
.input_style {
  padding: 9px 0px 7px 9px;
  font-size: 12px;
  width: 16rem;
  height: 3em;
  outline: none;
  background: #fafafa;
  border-radius: 3px;
  border: 1px solid #efefef;
}
.radio_style {
  display: inline;
  margin-right: auto;
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
  margin-top:20px;
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
