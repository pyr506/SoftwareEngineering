<template>
  <div>
    <h3 class="index_title">{{ title }}</h3>
    <hr />
  </div>
</template>
<script>
export default {
  data() {
    return {
      title: this.$route.name
    };
  }
};
</script>
<style scoped>
  .index_title {
    text-align: center;
    font-weight: bold;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;

  }
</style>
