<template>
  <footer class="page-footer font-small blue" style="margin-top:3rem; ">
    <div class="footer-copyright text-center py-3" style="width:70%;margin: 0 auto;">
      <div class="row">
        <div class="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-3 text-left" style="white-space:nowrap;">tel: {{ tel }} </div>
        <div class="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-3 text-left" style="white-space:nowrap;">e-mail: <a :href="'mailto:' + email">{{ email }}</a> </div>
        <div class="col-12 col-sm-12 col-md-12 col-lg-4 col-xl-6 text-left">address: {{ address }}</div>
      </div>
      <div>© 2020 Copyright: Taiwan-India Professional Expertise and Organization Cooperation Platform</div>
    </div>
  </footer>
</template>

<script>
import axios from "axios";
import { getWebinfos } from "../service/api.js";
export default {
  data() {
    return {
      tel: "",
      email: "",
      address: ""
    };
  },
  created() {
    getWebinfos().then(response => {
      this.tel = response.data.tel;
      this.email = response.data.email;
      this.address = response.data.address;
    });
  }
};
</script>
<style scoped>
footer {
  background-color: gainsboro;
  color: grey;
  text-align: center;
}
.LOGO {
  height: 96px;
  margin: 12px;
  padding: 0px;
}

@media (max-width: 576px) {
.webinfo {

}
}
</style>