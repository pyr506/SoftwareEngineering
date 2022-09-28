<template>
  <div id="app">
    <router-view style=" margin:auto;" />
  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<script>
export default {
  name: "App",
  components: {},
  computed: {
    // displayViewTitle() {
    //   if (
    //     this.$route.path == "/" ||
    //     this.$route.path == "/activities-page" ||
    //     this.$route.path == "/news-page" ||
    //     this.$route.path == "/news-page"
    //   ) {
    //     return false;
    //   } else {
    //     return true;
    //   }
    // }
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


