<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <div class="row">
        <div class="col">
          <h3 class="Members_title">Schools</h3>
        </div>
      </div>
      <div class="row">
        <div class="col-12 col-sm-12 col-md-12 col-xl">
          <div class="card">
            <div>
              <a href="https://www.ccu.edu.tw/" target="_blank"><img src="../assets/img/LOGO/CCU.png" alt="CCU" /></a>
            </div>
            <hr />
            <h3>National Chung Cheng University</h3>
          </div>
        </div>
        <div class="col-12 col-sm-12 col-md-12 col-xl">
          <div class="card">
            <div>
              <a href="https://www.iitp.ac.in/index.php/en-us/" target="_blank"><img src="../assets/img/Members/IIT_Ropar.png" alt="Indian Institute of Technology, Ropar"/></a>
            </div>
            <hr />
            <h3>Indian Institute of Technology, Ropar</h3>
          </div>
        </div>
        <div class="col-12 col-sm-12 col-md-12 col-xl">
          <div class="card">
            <div>
              <a href="https://www.chitkara.edu.in/" target="_blank"><img src="../assets/img/Members/Chitkara_University.jpg" alt="Chitkara University"/></a>
            </div>
            <hr />
            <h3>CHITKARA UNIVERSITY</h3>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <br>
          <br>
          <h3 class="Members_title">Industries</h3>
        </div>
      </div>
      <div class="row">
        <div class="col-12 col-sm-12 col-md-12 col-xl">
          <div class="card">
            <div>
              <a href="https://bestmarketingco.net/" target="_blank"><img src="../assets/img/Members/BMC.png" alt="BEST MARKETING COMPANY"/></a>
            </div>
            <hr />
            <h3>BEST MARKETING COMPANY</h3>
          </div>
        </div>
        <div class="col-12 col-sm-12 col-md-12 col-xl">
          <div class="card">
            <div>
              <a href="http://www.simco-groups.com/?fbclid=IwAR1JV7RZS71y58-hNZzB_qu-IU-lcngkst2AEQ4eEpzZkev_oBzt-EBZSwg" target="_blank"><img src="../assets/img/Members/SIMCO.png" alt="simco groups"/></a>
            </div>
            <hr />
            <h3>simco groups<br>&nbsp;<br></h3>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <br>
          <br>
          <a v-bind:href="'mailto:'+email"><img id="joinus" src="../assets/img/Members/Welcome_to_join_us.png" alt="simco groups"/></a>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import ViewTitle from "../components/ViewTitle.vue";
import { getWebinfos } from "../service/api.js";
export default {
  components: { ViewTitle },
  data() {
    return {
      email: ""
    };
  },
  created() {
    getWebinfos().then(response => {
      this.email = response.data.email;
    });
  }
};
</script>
<style  scoped>
.Members_title{
  text-align: center;
  color: #999;
  text-decoration:underline;
}
.card {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  max-width: 250px;
  margin: auto;
  text-align: center;
}
.card div{
  height:200px;
}
.card div img{
  max-width: 250px;
  max-height: 200px;
}
#joinus {
  width:100%;
}
</style>
