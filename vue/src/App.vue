<template>
  <div id="app">
        <el-header>
          <el-menu
            class="el-menu-demo"
            mode="horizontal"
            :default-active="$router.path"
            router
            background-color="#2F373C"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/" target="stock">股票</el-menu-item>
            <el-menu-item index="/fund" target="fund">基金</el-menu-item>
          </el-menu>
         
        </el-header>
        <router-view />
  </div>
</template>
<script>
export default {
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 0px;
}

.el-header {
  background-color: #2F373C;
  color: #333;
  text-align: left;
  line-height: 0px;
}
.el-footer {
  background-color: #000000;
  color: #333;
  text-align: left;
}
.el-aside {
  background-color: #2F373C;
  color: #333;
  text-align: left;
  line-height: 200px;
}
</style>


