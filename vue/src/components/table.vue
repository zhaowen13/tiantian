<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%"
      :cell-style="cellStyle"
      :header-cell-style="{ background: '#1F2021' }"
      :row-style="{
        background: '#4F4F4F',
        color: '#A4ADB3',
        fontweight: 'bold',
      }"
    >
      <el-table-column
        v-for="head in mydata.heads"
        :key="head.prop"
        :prop="head.prop"
        :label="head.label"
      >
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template #default="scope">
          <el-button
            type="danger"
            @click="del(scope.row)"
            icon="el-icon-delete"
            size="mini"
            circle
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin: 10px; float: right">
      <el-button
        type="primary"
        icon="el-icon-plus"
        @click="dialogFormVisible = true"
        round
        >添加{{ mydata.name }}</el-button
      >
    </div>
    <el-dialog title="添加基金(股票)" v-model="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="基金(股票)代码" :label-width="formLabelWidth">
          <el-input v-model="form.code" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="add()">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessageBox } from "element-plus";
import { ElMessage } from "element-plus";
import { ref, onMounted, onBeforeUnmount } from "vue";
export default {
  props: {
    data: {
      type: Object,
    },
  },
  setup(props) {
    const formLabelWidth = "120px";
    // console.log(props.data);
    const mydata = ref(props.data);
    var dialogFormVisible = ref(false);
    var form = ref({ code: "" });
    var tableData = ref([]);
    var websock = null;
    onMounted(() => {
      initWebSocket();
    });
    onBeforeUnmount(() => {
      websock.close();
    });
    return {
      formLabelWidth,
      dialogFormVisible,
      form,
      tableData,
      websock,
      mydata,
      del,
      add,
      cellStyle,
    };
    function add() {
      dialogFormVisible.value = false;
      ElMessage({
        type: "success",
        message: form.value.code + mydata.value.name + "添加成功!",
      });
      form.value.code = "";
    }
    function del(row) {
      ElMessageBox.confirm("是否删除" + row.name + mydata.value.name, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          ElMessage({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "已取消删除",
          });
        });
    }
    function initWebSocket() {
      //初始化weosocket
      const wsuri = "ws://127.0.0.1:8000/api/" + mydata.value.get_url;
      websock = new WebSocket(wsuri);
      websock.onmessage = websocketonmessage;
      websock.onopen = websocketonopen;
      websock.onerror = websocketonerror;
      websock.onclose = websocketclose;
    }
    function websocketonopen() {
      //连接建立之后执行send方法发送数据
      websock.send("");
    }
    function websocketonerror() {
      //连接建立失败重连
      initWebSocket();
    }
    function websocketonmessage(e) {
      //数据接收
      tableData.value = JSON.parse(e.data);
    }
    function websocketclose(e) {
      //关闭
      console.log("断开连接", e);
    }
    function cellStyle({ row, column }) {
      let cellStyle;
      if (row.quote_change.indexOf("-")) {
        cellStyle = "color: red;font-weight:bold";
      } else {
        cellStyle = "color: green;font-weight:bold";
      }
      if (column.label == "涨跌幅") return cellStyle;
    }
  },
};
</script>
<style>
.el-button {
  margin: 0;
}
.el-table tbody tr:hover>td { 
    background-color:#3C3C3C!important
}

.el-table--border,
.el-table--group {
  border: none;
}
.el-table__header-wrapper th:nth-last-of-type(2) {
  border-right: none;
}
.el-table--border td:nth-last-of-type(1) {
  border-right: none;
}
.el-table td,
.el-table th.is-leaf {
  border: none;
}
.el-table--border::after,
.el-table--group::after {
  width: 0;
}
</style>