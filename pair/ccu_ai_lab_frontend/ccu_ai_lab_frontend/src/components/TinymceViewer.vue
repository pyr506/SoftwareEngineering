<template>
  
  <editor
    api-key="xlvgpsk327zddyaa8c34iduncmuxrnts8wom72v1ls64lfqn"
    v-model="myValue"
    :init="{
      menubar: false,
      toolbar: false,
      statusbar: false,
      plugins: [
      'autoresize advlist autolink lists link image charmap print preview anchor',
      'searchreplace visualblocks code fullscreen',
      'insertdatetime media table paste code help wordcount'
      ],
      toolbar: []
    }"
    :disabled="true"
    />
</template>

<script>
import Editor from '@tinymce/tinymce-vue'

export default {
  components: {
    'editor': Editor,
  },
  props: {
    //傳入一個value，使元件支援v-model繫結
    value: {
        type: String,
        default: ''
    },
  },
  data() {
    return {
      myValue: this.value
    }
  },
  watch: {
    value(newValue) {
        this.myValue = newValue
    },
    myValue(newValue) {
        this.$emit('input', newValue)
    }
  },
  created() {
    
  }
}
</script>