<template>
  <div id="app">
    <Header></Header>
    <b-container class="pageContainer">
      <b-row>
        <b-col class="col-12 col-sm-12 col-md-3">
          <SideNav></SideNav>
          <SideNavUser v-if="isLogin()"></SideNavUser>
        </b-col>
        <b-col class="col-12 col-sm-12 col-md-9">
          <router-view style=" margin:auto;" />
          <Chat v-if="isLogin()" />
        </b-col>
      </b-row>
    </b-container>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import SideNav from "./components/SideNav.vue";
import Chat from "./views/Chat.vue";
// import ViewTitle from "./components/ViewTitle.vue";
import SideNavUser from "./components/SideNavUser.vue";

export default {
  name: "App",
  components: {
    Header,
    Footer,
    SideNav,
    SideNavUser,
    Chat
  },
  methods: {
    isLogin() {
      return this.$store.state.isLogin;
    }
  }
};
</script>

<style>
#app {
  font-family: Helvetica, 微軟正黑體, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
}
.pageContainer {
  min-height: 750px;
}
.contentBox {
  padding: 5px;
  margin: 5px;
}
.content {
  text-indent: 2em;
  padding: 20px;
  text-align: justify;
  text-justify: inter-ideograph;
}
.post-detail {
  color: gray;
  font-size: 13px;
  padding: 25px;
}
.admin-link {
  padding: 10px;
  margin-bottom: 20px;
}

/* The navigation menu links */
.link {
  text-decoration: none;
  color: #818181;
}

/* When you mouse over the navigation links, change their color */
.link:hover {
  color: #4ca4ec;
}
td {
  color: #9b9771;
  font-size: 17px;
}

</style>


