<template>
  <div>
    <div>
      <h3 class="index_title">Category Lists</h3>
      <hr />
    </div>
    <div class="sidenav border">
      <router-link :to="{ name: 'News'}">News</router-link>
      <router-link :to="{ name: 'Events'}">Events</router-link>
      <router-link :to="{ name: 'Members'}">Members</router-link>
      <router-link :to="{ name: 'About'}">About us</router-link>
      <router-link v-if="!isLogin()" :to="{ name: 'Register rules'}">Register</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    isLogin() {
      this.username = localStorage.getItem("username");
      return this.$store.state.isLogin;
    }
  },
};
</script>

<style scoped>
  .index_title {
    text-align: center;
    font-weight: bold;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;

  }
.sidenav {
  z-index: 1; /* Stay on top */
  overflow-x: hidden; /* Disable horizontal scroll */
  padding: 20px 0px;
  text-align: center;
}
/* The navigation menu links */
.sidenav a {
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 20px;
  color: #818181;
  display: block;
}

/* When you mouse over the navigation links, change their color */
.sidenav a:hover {
  color: #86baa1;
}

/* On smaller screens, where height is less than 450px, change the style of the sidebar (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidenav {
    padding-top: 15px;
  }
  .sidenav a {
    font-size: 18px;
  }
}
</style>