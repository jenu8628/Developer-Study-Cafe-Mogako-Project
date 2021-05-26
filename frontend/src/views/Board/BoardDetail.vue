<template>
  <div class="boarddetail-contailner">
    <div class="boarddetail-box">
      <!-- 뒤로가기 -->
      <i @click="back" class="back cursor fas fa-arrow-alt-circle-left"></i>
      <!-- 제목/ 생성시간 -->
      <div class="article-title">
        <div>
          {{title}}
        </div>
        <div class="article-create">
          {{date}} 
          {{time}}
        </div>
      </div>
      <!-- 작성자/ 조회수 -->
      <div class="article-writer">
        <div class="article-username">{{username}}</div>
        <div class="article-view">
          <div class="view-a"> 조회 수 </div>
          <div class="view-b"> {{articleDetail.viewed_num}}</div>
        </div>
      </div>
      <!-- 내용 -->
      <div class="article-content">
        {{articleDetail.content}}
      </div>
      <!-- 댓글 -->
      <div class="comment-title">댓글</div>
      <!-- 댓글 등록 -->
      <div class="comment-input">
        <input
          v-model="comment" 
          type="text" 
          class="text-input" 
          @keyup.enter="createComment"
          placeholder="댓글 입력"
        >
        <div @click="createComment" class="cursor input-btn">입력</div>
      </div>
      <!-- 댓글 내용 -->
      <div 
        class="article-comment"
        v-for="(comment, index) in articleDetail.comments"
        :key="index"
      >
        <div class="comment-flex">
          <div class="comment-flex-margin">{{comment.writer.username}}</div>
          <div class="comment-create">
            <div class="comment-create-a created"> {{comment.created_at[0]}} </div>
            <div class="created"> {{comment.created_at[1]}} </div>
          </div>
        </div>
        <div>{{comment.content}}</div>
        <i 
          @click="deleteComment(comment.id)" 
          v-if="comment.writer.id === myId" 
          class="cursor absolute fas fa-trash-alt"
          >
        </i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      // boardId : "1",
      boardId : this.$route.query.title,
      articleId: this.$route.query.body,
      title : "",
      date : "",
      time : "",
      articleDetail :[],
      username : "",
      profile : "",
      comment : "",
      comments: [],
      myId : parseInt(localStorage.getItem('user_id'))
    }
  },
  mounted() {
    window.scrollTo(0,0)
    this.getArticleDetail()
  },
  methods: {
    getArticleDetail () {
      axios.get(`https://k4b205.p.ssafy.io:7799/board/${this.boardId}/article/${this.articleId}/`)
      .then((res)=> {
        this.title = res.data.title

        res.data.created_at = [
          res.data.created_at.substring(0,10),
          res.data.created_at.substring(11,16)
        ]
        this.date = res.data.created_at[0]
        this.time = res.data.created_at[1]

        for (let i = 0; i < res.data.comments.length; i++) {
          res.data.comments[i].created_at = [
            res.data.comments[i].created_at.substring(0,10),
            res.data.comments[i].created_at.substring(11,16)
          ]
        }
        
        this.articleDetail = res.data
        axios.get(`https://k4b205.p.ssafy.io:7799/user/profile/${this.articleDetail.writer.id}/`)
        .then((response)=>{
          this.username = response.data.username
          this.profile = response.data.profile_image
        })
      })
    },
    createComment() {
      if (this.comment !== ""){
        const config = this.setToken()
        const data = {
          "title" : this.boardId,
          "content" : this.comment
        }
        const boardId = parseInt(this.boardId)
        const articleId = parseInt(this.articleId)
        axios.post(`https://k4b205.p.ssafy.io:7799/board/${boardId}/article/${articleId}/comment/`,data, config)
        .then(()=> {
          this.comment = ""
          this.getArticleDetail()
        })
      }
    },
    deleteComment(event) {
      const config = this.setToken()
      axios.delete(`https://k4b205.p.ssafy.io:7799/board/${this.boardId}/article/${this.articleId}/comment/${event}`, config)
      .then(()=> {
        this.getArticleDetail()
      })
    },
    back() {
      history.go(-1)
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
  },
}
</script>

<style scoped>
.boarddetail-contailner{
  margin-top: 30px;
  width: 100%;
  min-height: 100vh;
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
}
.boarddetail-contailner .cursor:hover{
  cursor: pointer;
}
.boarddetail-contailner .boarddetail-box {
  width: 80%;
}
.boarddetail-contailner .boarddetail-box .back{
  font-size: 2.5rem;
  margin-bottom: 30px;
}
/* 첫 줄 */
.boarddetail-contailner .boarddetail-box .article-title{
  font-size: 1.5rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  display: flex;
  justify-content: space-between;
  border-bottom: black 1px solid;
  padding-left: 10px;
}
.boarddetail-contailner .boarddetail-box .article-title .article-create{
  display: flex;
  align-items: center;
  margin-right: 10px;
  font-size: 0.8rem;
}

/* 두번째 줄 */
.boarddetail-contailner .boarddetail-box .article-writer{
  font-size: 1rem;
  margin-bottom: 30px;
  padding-bottom: 20px;
  display: flex;
  justify-content: space-between;
  border-bottom: black 1px solid;
  padding-left: 10px;
}
.boarddetail-contailner .boarddetail-box .article-writer .article-view{
  display: flex;
  justify-content: space-between;
}
.boarddetail-contailner .boarddetail-box .article-writer .article-view .view-a{
  margin-right: 10px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}
.boarddetail-contailner .boarddetail-box .article-writer .article-view .view-b{
  margin-right: 10px;
}


/* 세번째 줄 */
.boarddetail-contailner .boarddetail-box .article-content{
  font-size: 1.1rem;
  padding-left: 10px;
  border-bottom: black 1px solid;
  margin-bottom: 30px;
  padding-bottom: 30px;
}

/* 댓글 */
.boarddetail-contailner .boarddetail-box .comment-title{
  font-size: 1.2rem;
  padding-left: 10px;
  margin-bottom: 30px;
}
.boarddetail-contailner .boarddetail-box .comment-input{
  display: flex;
  margin-bottom: 15px;
}
.boarddetail-contailner .boarddetail-box .comment-input .text-input{
  border-top: none;
  border-left: none;
  border-right: none;
  width: 70%;
  transition: ease 0.5s;
}
.boarddetail-contailner .boarddetail-box .comment-input .text-input:focus{
  outline: none;
  border-bottom: 2px solid #aac3eb;
}
/* 버튼 */
.boarddetail-contailner .boarddetail-box .comment-input .input-btn{
  border: 1px solid #aac3eb;
  margin-left: 10px;
  background: #aac3eb;
  border-radius: 10px;
  width: 50px;
  height: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: ease 0.5s;
}
.boarddetail-contailner .boarddetail-box .article-comment {
  border-bottom: 1px black solid;
  margin-bottom: 10px;
  padding-bottom: 5px;
  position: relative;
}

.boarddetail-contailner .boarddetail-box .article-comment .comment-flex{
  display: flex;
  margin-bottom: 10px;
}
.boarddetail-contailner .boarddetail-box .article-comment .comment-create{
  display: flex;
  align-items: center;
}
.boarddetail-contailner .boarddetail-box .article-comment .comment-flex .comment-flex-margin{
  margin-right: 30px;
}
.boarddetail-contailner .boarddetail-box .article-comment .comment-create-a{
  margin-right: 10px;
}
.boarddetail-contailner .boarddetail-box .article-comment .created{
  font-size: 0.8rem;
  color: rgb(114, 114, 114);
}
.boarddetail-contailner .boarddetail-box .article-comment .absolute{
  position: absolute;
  right: 20px;
  top: 20px;
}


</style>