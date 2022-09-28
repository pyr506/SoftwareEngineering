<template>
  <div>
    <ViewTitle></ViewTitle>

    <div class="contentBox">
      <b-form>
        <b-form-group id="input-group-1" label="Title:" label-for="input-1">
          <b-form-input id="input-1" v-model="title" type="text" required></b-form-input>
        </b-form-group>
        <div>
          <TinymceEditor ref="editor"
            v-model="content"
          >
          </TinymceEditor>
        </div>
        <div class="text-center">
          <a class="btn btn-primary text-white" @click="onSubmit()" variant="primary">Save</a>
        </div>
      </b-form>
    </div>
    <div class="text-right post-detail">
      <div>Clicked: {{ clicked }}</div>
      <div>Created Date (GMT):{{ created_at }}</div>
      <div>Updated Date (GMT):{{ updated_at }}</div>
    </div>
    <div class="text-right contentBox">
      <b-button pill variant="outline-secondary" @click="$router.go(-1)">back</b-button>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { getEventDetail, editEvent } from "../../service/api.js";
import ViewTitle from "../../components/ViewTitle.vue";
import TinymceEditor from '../../components/TinymceEditor.vue'
export default {
  components: { ViewTitle, TinymceEditor },
  data() {
    return {
      id: window.location.hash.split("/")[3],
      title: "",
      content: "",
      clicked: "",
      created_at: "",
      updated_at: "",

      user: localStorage.getItem("role_id"),
    };
  },
  methods: {
    onSubmit() {
      editEvent(this.id, this.title, this.content)
        .then(response => {
          if (response.status == 'error')
          {
            throw new Error(response.message);
          }
          alert("Save Event Success");
          const backURL = "/" + window.location.hash.split("/")[1];
          this.$router.push(backURL);
        })
        .catch(error => {
          alert("Save Event Error: " + error.message);
          console.log(error);
        });
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        this.$router.push("/events/");
      }
    },
  },
  created() {
    getEventDetail(window.location.hash.split("/")[3]).then(response => {
      this.title = response.data.title;
      this.content = response.data.content;
      this.clicked = response.data.clicked;
      this.created_at = response.data.created_at;
      this.updated_at = response.data.updated_at;
    });
    this.isAdmin();
  }
};
</script>
