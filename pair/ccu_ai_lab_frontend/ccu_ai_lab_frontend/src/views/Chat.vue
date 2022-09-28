<template>

<main id="app">
	<section>
		<div v-show="showBnt">
			<div class = "start_buttom">
				<img src="../assets/img/chat.png" class="open-button2" @click="openForm">
			</div>
		</div>
		<div v-show="isShow">
			<div class="chat-box">
				<div class="chat-box-header" @click="openForm">
					ChatBot
				</div>
				<div class="chat-box-body">
					<div class="chat-box-overlay">   
					</div>
						
					<div ref="chatArea" class="chat-area">
							<div v-for="message in messages" :key="message.id" class="message" :class="{ 'message-out': message.author === 'you', 'message-in': message.author !== 'you' }">
								<div calss="in-message" :class="{'message-out-t': message.author === 'you', 'message-in-t': message.author !== 'you'}" v-html="message.body">
								</div>
								<img v-if="message.id >= 0" src="../assets/img/report.png" class="out-none reply" @click="reply_error(message.id)">
							</div>
		
					</div>
				</div>
				<div class="chat-input">      
					<form @submit.prevent="sendMessage('out')" id="person2-form">
						<input v-model="youMessage" id="person2-input" type="text" placeholder="Type your message">
					
						<button type="submit" class="chat-submit" id="chat-submit">send</button>
					</form>      
				</div>
			</div>
		</div>
	</section>
</main>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import { echomsg,querymsg,send_error } from "../service/api.js";
export default {
	data() {
		return {
			guideCnt: 0,
			chatID: 0,
			youCnt: 0,
			bobMessage: '',
			youMessage: '',
			messages: [
			],
			isShow: false,
			showBnt: true,
		}
	},
	mounted:function(){
        this.getMessages();
	},
	methods: {
		openForm(){
			this.isShow = !this.isShow;
			this.showBnt = !this.showBnt;
		},
		reply_error: function(id){
			alert("thanks for reply");
			send_error(id);
		},
		sendMessage(direction) {
			if (!this.youMessage && !this.bobMessage) {
				return;
			}
			if (direction === 'out') {
				this.messages.push({
					id: 'you' + this.youCnt,
					body: this.youMessage,
					author: 'you'
				});

				echomsg(this.youMessage,localStorage.getItem("id"),localStorage.getItem("token"))
					.then((response) => {
					this.bobMessage = response.data.msg;
					this.chatID = response.data.id;
					this.sendMessage('in');
				}).catch((error) => {
					console.log(error);
				});
				

				this.youMessage = '';
				this.youCnt++;
			} else if (direction === 'in') {
				this.messages.push({
					id: this.chatID,
					body: this.bobMessage,
					author: 'bob'
				});
				this.bobMessage = '';
				this.bobCnt++;
			} else {
				alert('something went wrong');
			}
			Vue.nextTick(() => {
				let messageDisplay = this.$refs.chatArea;
				messageDisplay.scrollTop = messageDisplay.scrollHeight;
			})
		},
		
		clearAllMessages() {
			this.messages = [];
		},
		fakesendMessage(direction){
			if (direction === 'out') {
				this.messages.push({
					id: 'you' + this.youCnt,
					body: this.youMessage,
					author: 'you'
				});
				this.youMessage = '';
				this.youCnt++;
			}
			Vue.nextTick(() => {
				let messageDisplay = this.$refs.chatArea;
				messageDisplay.scrollTop = messageDisplay.scrollHeight;
			})
		},
		getMessages() {
			querymsg(localStorage.getItem("id"),localStorage.getItem("token"))
				.then((response) => {
					const guide = response.data.guide;
					const data = response.data.msg;
					var result = data.length;

					// print guidelines
					this.bobMessage = guide;
					this.chatID = (--this.guideCnt) ;
					this.sendMessage('in');		
					
					// print chat record
					for (var i = 0; i<result ; i++){
						this.youMessage = data[i]['user_content'];
						this.fakesendMessage('out');
						this.bobMessage = data[i]['ai_content'];
						this.chatID = data[i]['id'];
						this.sendMessage('in');
					}
				}).catch((error) => {
					console.log(error);
				});
		}
	}
}

</script>

<style>

.reply {
  width: 1.25rem;
  margin-top: 16px;
  cursor: pointer;
}

.chat-box {
  display:block;
  background: #efefef;
  position:fixed;
  right:30px;
  bottom:50px;  
  width:350px;
  max-width: 85vw;
  max-height:100vh;
  border-radius:5px;  
/*   box-shadow: 0px 5px 35px 9px #464a92; */
  box-shadow: 0px 5px 35px 9px #ccc;
}
.chat-box-toggle {
  float:right;
  margin-right:15px;
  cursor:pointer;
}
.chat-box-header {
  cursor:pointer;
  background: #5A5EB9;
  height:55px;
  border-top-left-radius:5px;
  border-top-right-radius:5px; 
  color:white;
  text-align:center;
  font-size:20px;
  padding-top:17px;
}
.chat-box-body {
  position: relative;  
  height:420px;  
  /*height:auto;*/
  border:1px solid #ccc;  
  overflow: hidden;
}
.chat-box-body:after {
  content: "";
  opacity: 0.1;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  height:100%;
  position: absolute;
  z-index: -1;   
}
#person2-input {
  background: #f4f7f9;
  width:100%; 
  position:relative;
  height:47px;  
  padding-top:10px;
  padding-right:50px;
  padding-bottom:10px;
  padding-left:15px;
  border:none;
  resize:none;
  outline:none;
  border:1px solid #ccc;
  color:#888;
  border-top:none;
  border-bottom-right-radius:5px;
  border-bottom-left-radius:5px;
  overflow:hidden;  
}
.person2-input > form {
    margin-bottom: 0;
}
#person2-input::-webkit-input-placeholder { /* Chrome/Opera/Safari */
  color: #ccc;
}
#person2-input::-moz-placeholder { /* Firefox 19+ */
  color: #ccc;
}
#person2-input:-ms-input-placeholder { /* IE 10+ */
  color: #ccc;
}
#person2-input:-moz-placeholder { /* Firefox 18- */
  color: #ccc;
}
.chat-submit {  
  position:absolute;
  bottom:3px;
  right:18px;
  background: transparent;
  box-shadow:none;
  border:none;
  border-radius:50%;
  color:#5A5EB9;
  width:35px;
  height:35px;  
}
.chat-logs {
  padding:15px; 
  height:370px;
  overflow-y:scroll;
}

.chat-logs::-webkit-scrollbar-track
{
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  background-color: #F5F5F5;
}

.chat-logs::-webkit-scrollbar
{
  width: 5px;  
  background-color: #F5F5F5;
}

.chat-logs::-webkit-scrollbar-thumb
{
  background-color: #5A5EB9;
}

.cm-msg-text {
  background:white;
  padding:10px 15px 10px 15px;  
  color:#666;
  max-width:75%;
  float:left;
  margin-left:10px; 
  position:relative;
  margin-bottom:20px;
  border-radius:30px;
}/*
.message-in .message-out {
  background:white;
  padding:10px 15px 10px 15px;  
  color:#666;
  max-width:75%;
  float:left;
  margin-left:10px; 
  position:relative;
  margin-bottom:20px;
  border-radius:30px;
}*/
.chat-msg {
  clear:both;    
}
.chat-msg.self > .cm-msg-text {  
  float:right;
  margin-right:10px;
  background: #5A5EB9;
  color:white;
}/*
.message-in { 
  float:right;
  margin-right:10px;
  background: #5A5EB9;
  color:white;
}*/
.cm-msg-button>ul>li {
  list-style:none;
  float:left;
  width:50%;
}
.cm-msg-button {
  clear: both;
  margin-bottom: 70px;
}


.submit-buttom {
	margin-left: .5rem;
}

.headline {
	text-align: center;
	font-weight: 100;
	color: white;
}

.chat-area {
	/*   border: 1px solid #ccc; */
	background: #efefef;
	height: 45vh;
	padding: 1em;
	overflow: auto;
	max-width: 360px;
	margin: 0 auto 0 auto;
	/* box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3 ) */
}

.message {
	width: 45%;
	/*border-radius: 10px;*/
	/*padding: .5rem;*/
	/*margin:  .5rem;*/
	/*   margin-bottom: .5em; */
	font-size: 1em;
}

.message-out {
	/*margin-left: 50%;*/
	width: 100%;
	/*width: min-content;*/
	float: right;
}

.message-out > .out-none {
	display: none;
}

.message-out-t {
	padding: .5rem;
	margin:  .5rem;
	color: white;	
	border-radius: 10px;
	background: #5A5EB9;
	max-width: 80%;
	float: right;
	text-align: left;
	overflow-wrap: break-word;
}

.message-in-t {
	border-radius: 10px;
	background: #FFFFFF;
	padding: .5rem;
	margin:  .5rem;
	max-width: 80%;
	float: left;
	overflow-wrap: break-word;

}

.message-in {
	width: 100%;
	color: black;
	float: left;
}

.chat-inputs {
	display: flex;
	justify-content: space-between;
}

#person1-input {
	padding: .5em;
}

#person2-input-temp {
	padding: .5em;
	margin-bottom: .5rem;
	max-width: 13rem;
}

.open-button {
	background-color: #555;
	color: white;
	padding: 16px 20px;
	border: none;
	cursor: pointer;
	opacity: 0.8;
	position: fixed;
	bottom: 23px;
	right: 28px;
	width: 280px;
}

.open-button2 {
	cursor: pointer;
	opacity: 0.8;
	position: fixed;
	bottom: 23px;
	right: 28px;
	width: 100px;
}

@media (max-width: 800px) {
	.open-button2 {
		width: 70px;
	}
	
	.chat-box{
		width:300px;
	}
}

@media (max-width: 400px) {
	.open-button2 {
		width: 50px;
	}
}

.chat-popup {
	//display: none;
	position: fixed;
	bottom: 0;
	right: 15px;
	border: 3px solid #f1f1f1;
	z-index: 9;
}

/* Add styles to the form container */
.form-container {
	max-width: 300px;
	padding: 10px;
	background-color: white;
}

/* Full-width textarea */
.form-container textarea {
	width: 100%;
	padding: 15px;
	margin: 5px 0 22px 0;
	border: none;
	background: #f1f1f1;
	resize: none;
	min-height: 200px;
}

/* When the textarea gets focus, do something */
.form-container textarea:focus {
	background-color: #ddd;
	outline: none;
}

/* Set a style for the submit/send button */
.form-container .btn {
	background-color: #04AA6D;
	color: white;
	padding: 16px 20px;
	border: none;
	cursor: pointer;
	width: 100%;
	margin-bottom:10px;
	opacity: 0.8;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
	background-color: red;
}

/* Add some hover effects to buttons */
.form-container .btn:hover, .open-button:hover {
	opacity: 1;
}
</style>
