<template>
<div class="main">
  <div class="login">
    <div class="ms-title">后台管理系统</div>
    <el-form
      :model="ruleForm"
      status-icon
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item prop="user" size="medium ">
        <el-input placeholder="请输入用户名" v-model="ruleForm.user" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item prop="pass" size="medium">
        <el-input type="password" placeholder="请输入密码" v-model="ruleForm.pass" autocomplete="off"></el-input>
      </el-form-item>
       <div>
      <br />
        <span style="color:red">{{message}}</span>
      </div>
      <el-form-item id="login-btn" size="small">
        <el-button type="primary" size="small" style="width:200px" @click="submitForm()">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    var validateuser = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入用户名"));
      }
    };
    var validatepass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      }
    };
    return {
      message: "",
      ruleForm: {
        user: "",
        pass: "",
      },
      rules: {
        user: [{ validator: validateuser, trigger: "blur" }],
        pass: [{ validator: validatepass, trigger: "blur" }],
      },
    };
  },
  methods: {
    submitForm() {
      this.$ajax
        .post("api/login", {
          username: this.ruleForm.user,
          password: this.ruleForm.pass,
        })
        .then((res) => {
          if (res.data["status"]) {
            localStorage.setItem(
              "Authorization",
              JSON.stringify(res.data["token"])
            );
            this.$router.push("/test");
            this.$router.go(0);
            this.$message({
            message: "  成功",
            type: "success",
          });
          } else {
            this.message = res.data["msg"];
          }
        });
    },
  },
};
</script>
<style >
.main{
  width: 100%;
  height: 100%;
  background: url("~@/assets/timg.jpg") center center no-repeat;
  background-size: 100% 100%;
}
.login {
  position: absolute;
  left: 45%;
  top: 50%;
  width: 500px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
 
  overflow: hidden;
  
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 25px;
  font-weight: 600;
}

.demo-ruleForm {
  padding: 30px 0px;
}
.el-form-item {
  width: 400px;
  text-align: center;
}
</style>