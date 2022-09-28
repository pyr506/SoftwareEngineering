<template>
  <div>
    <div class="text-center">
      <hr />
    </div>
    <div class="sidenav border">
      <router-link :to="{ name: 'Projects'}">Projects</router-link>
      <router-link :to="{ name: 'Add Project'}">New Project</router-link>
      <router-link :to="{ name: 'My Account'}">My Account</router-link>
      <router-link :to="{ name: 'Help'}">Help</router-link>
      <!-- <router-link :to="{ name: 'Contact'}">會員回報</router-link> -->
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>

<style scoped>
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