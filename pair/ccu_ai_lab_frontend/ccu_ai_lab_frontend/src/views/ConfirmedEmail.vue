<template>
  <div>Confirm Email Page</div>
</template>

<script>
import axios from "axios";
import { confirmed_email } from "../service/api.js";
export default {
  data() {
    return {};
  },
  methods: {
    onSubmit() {
      confirmed_email(
        window.location.hash.split("/")[3],
        window.location.hash.split("/")[4]
      )
        .then((resp) => {
          console.log(resp);
          if (resp.status == "error") {
            throw new Error(resp.message);
          }
          localStorage.token = resp.data.access_token;
          alert("Email verification has been successful!");

          this.$store.state.isLogin = true;
          localStorage.setItem("token", resp.data.access_token);
          localStorage.setItem("id", resp.data.user.id);
          localStorage.setItem("username", resp.data.user.username);
          if (resp.data.user.role == "Administrator") {
            localStorage.setItem("role_id", 3);
          } else if (resp.data.user.role == "Moderator") {
            localStorage.setItem("role_id", 2);
          } else if (resp.data.user.role == "User") {
            localStorage.setItem("role_id", 1);
          }
          this.$router.push("/");
          window.location.reload();
        })
        .catch((error) => {
          console.log(error);
          alert("Email Verification Error: " + error.message);
          this.$router.push("/");
          window.location.reload();
        });
    },
  },
  created() {
    this.onSubmit();
  },
};
</script>
