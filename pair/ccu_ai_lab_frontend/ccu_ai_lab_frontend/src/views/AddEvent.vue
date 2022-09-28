<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form>
        <b-form-group id="input-group-1" label="Event Title:" label-for="input-1">
          <b-form-input id="input-1" v-model="form.title" type="text" required></b-form-input>
        </b-form-group>

        <div>
          <TinymceEditor ref="editor"
            v-model="form.content"
          >
          </TinymceEditor>
        </div>

        <div class="text-center">
          <button class="btn btn-primary text-white" @click="onSubmit()" variant="primary" :disabled="isDisabled">Add</button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { newEvent } from "../service/api.js";
import ViewTitle from "../components/ViewTitle.vue";
import TinymceEditor from '../components/TinymceEditor.vue'

export default {
  components: {
    ViewTitle,
    TinymceEditor
  },
  data() {
    return {
      form: {
        title: "",
        content: ""
      },
      isDisabled: false,
      user: localStorage.getItem("role_id"),
    };
  },
  methods: {
    onSubmit() {
      this.isDisabled=true;
      newEvent(this.form.title, this.form.content)
        .then(response => {
          if (response.status == 'error')
          {
            throw new Error(response.message);
          }
          alert("Add Event Success: " + this.form.title);
          const backURL = "/" + window.location.hash.split("=")[1];
          this.$router.push(backURL);
        })
        .catch(error => {
          alert("Add Event Error: " + error.message);
          console.log(error);
          this.isDisabled=false;
        })
        .finally(function(){this.isDisabled=false});
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        this.$router.push("/events/");
      }
    }
  },
  created() {
    this.isAdmin();
  }
};
</script>
