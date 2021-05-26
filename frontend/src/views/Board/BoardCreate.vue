<template>
  <div class="boardCreate-container">
    <!-- 제목 -->
    <input 
      class="input-font text-input"
      v-model="form.title" 
      type="text"
      placeholder="제목을 입력하세요."
    >
    <!-- 내용 -->
    <textarea 
      name="content"
      class="input-font textarea-input"
      v-model="form.content"
      cols="30" rows="15" 
      placeholder="내용을 입력하세요."
    >
    </textarea>

    <!-- 버튼 -->
    <div class="btn-box">
      <i @click="createArticle" class="boardCreate-btn fas fa-check-circle"></i>
      <i @click="locationBack" class="boardCreate-btn fas fa-times-circle"></i>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      boardId : this.$route.query.title,
      studyId : this.$route.query.body,
      form : {
        title : '',
        content : '',
      },
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
    createArticle () {
      const config = this.setToken()
      if (this.form.title.length === 0) {
        alert('제목을 입력해주세요!')
      } else if (this.form.content.length === 0) {
        alert('내용을 입력해주세요!')
      } else {
        axios.post(`https://k4b205.p.ssafy.io:7799/board/${this.boardId}/article/`,this.form ,config)
        .then(()=>{
          this.$router.push({
            name:"BoardList",
            query: {
              title : this.studyId
            }
          })
        })
      }
    },
    locationBack(){
      history.go(-1);
    }
  },
  mounted() {
    window.scrollTo(0,0)
  },
}
</script>

<style scoped>
.boardCreate-container {
  width: 60%;
  display: flex;
  margin: auto;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  padding-bottom: 10vh;
}

.boardCreate-container .input-font {
  font-size: 1rem;
  font-weight: bold;
}

/* 제목 css */
.boardCreate-container .text-input {
  border-top: none;
  border-left: none;
  border-right: none;
  transition: 0.5s ease;
  background: none;
  margin-top: 100px;
}
.boardCreate-container .text-input:focus{
  outline: none;
  border-bottom: 2px solid #aac3eb;
  box-shadow: 5px 5px 5px 1px #c6d6f079;
}

/* 내용 css */
.boardCreate-container .textarea-input{
  margin-top: 50px;
  transition: 0.5s ease;
  background: none;
  border: 2px solid rgba(0, 0, 0, 0.486);
}
.boardCreate-container .textarea-input:focus{
  outline: none;
  border: 2px solid #aac3eb;
  box-shadow: 5px 5px 5px 1px #c6d6f079;
}

/* 버튼 css */
.boardCreate-container .btn-box{
  margin-top: 3vh;
  display: flex;
  justify-content: space-evenly;
}
.boardCreate-container .boardCreate-btn{
  transition: ease 0.5s;
  font-size: 2rem;
  color: #465061;
}
.boardCreate-container .boardCreate-btn:hover{
  cursor: pointer;
  transform: scale(1.3);
}
</style>