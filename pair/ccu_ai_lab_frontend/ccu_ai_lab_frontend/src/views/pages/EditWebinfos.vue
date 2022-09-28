<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form>
        <b-form-group id="input-group-1" label="tel:" label-for="input-1">
          <b-form-input id="input-1" v-model="tel" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-1" label="e-mail:" label-for="input-1">
          <b-form-input id="input-1" v-model="email" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-1" label="address:" label-for="input-1">
          <b-form-input id="input-1" v-model="address" type="text" required></b-form-input>
        </b-form-group>
        <div class="text-center">
          <a class="btn btn-primary text-white" @click="onSubmit()" variant="primary">Save</a>
        </div>
      </b-form>
    </div>
    <div class="text-right contentBox">
      <b-button pill variant="outline-secondary" @click="$router.go(-1)">back</b-button>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { getWebinfos, editWebinfos } from "../../service/api.js";
import ViewTitle from "../../components/ViewTitle.vue";
export default {
  components: { ViewTitle },
  data() {
    return {
      tel: "",
      email: "",
      address: "",
      
      user: localStorage.getItem("role_id")
    };
  },
  methods: {
    onSubmit() {
      editWebinfos(this.tel, this.email, this.address)
        .then(response => {
          if (response.status == 'error')
          {
            throw new Error(response.message);
          }
          alert("Save Webinfos Success");
          this.$router.push("/my_account");
        })
        .catch(error => {
          alert("Save Webinfos Error: " + error.message);
          console.log(error);
        });
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        this.$router.push("/my_account/");
      }
    }
  },
  created() {
    getWebinfos().then(response => {
      this.tel = response.data.tel;
      this.email = response.data.email;
      this.address = response.data.address;
    });
    this.isAdmin();
  }
};
</script>
