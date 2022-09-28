<template>
  <editor
    api-key="xlvgpsk327zddyaa8c34iduncmuxrnts8wom72v1ls64lfqn"
    v-model="myValue"
    :init="{
      height: 800,
      browser_spellcheck: true,
      menubar: false,
      branding: false,
      statusbar: false,

      paste_retain_style_properties: 'all',
      paste_word_valid_elements: '*[*]', // word
      paste_data_images: true, // 貼時能把内容裡的圖自動上傳，非常强的功能
      paste_convert_word_fake_lists: false, // 插入word需要該屬性
      paste_webkit_styles: 'all',
      paste_merge_formats: true,
      nonbreaking_force_tab: false,
      paste_auto_cleanup_on_paste: false,
      paste_remove_styles_if_webkit: false,

      plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount',
      ],
      toolbar: [
        'undo redo | formatselect | fontsizeselect | bold italic forecolor backcolor | \
        alignleft aligncenter alignright alignjustify | ',
        'bullist numlist outdent indent | link table image | removeformat | help',
      ],

      images_upload_handler: my_image_upload_handler,
      images_reuse_filename: false,
      automatic_uploads: true,
    }"
  />
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import { uploadImage } from "../service/api.js";

export default {
  components: {
    editor: Editor,
  },
  props: {
    //傳入一個value，使元件支援v-model繫結
    value: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      myValue: this.value,
    };
  },
  methods: {
    my_image_upload_handler(blobInfo, success, failure, progress) {
      uploadImage(blobInfo.blob())
        .then((response) => {
          if (response.status == "error") {
            throw new Error(response.message);
          }
          const data = response.data;
          success(
            "https://127.0.0.1/center/center/assets/img/upload/" +
              data[0]["location"]
          );
        })
        .catch((error) => {
          failure("Upload Image Error:" + error);
          return;
        });
    },
  },
  watch: {
    value(newValue) {
      this.myValue = newValue;
    },
    myValue(newValue) {
      this.$emit("input", newValue);
    },
  },
};
</script>