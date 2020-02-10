 <template>
  <div>
      <el-table :data="market" stripe style="width: 100%">
      <el-table-column prop="name" label="股票名称" width="180"></el-table-column>
      <el-table-column prop="stockcode" label="股票代码" width="180"></el-table-column>
      <el-table-column prop="latestprice" label="最新价"></el-table-column>
      <el-table-column prop="quotechange" label="涨跌幅"></el-table-column>
    </el-table>
    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column prop="name" label="基金名称" width="180"></el-table-column>
      <el-table-column prop="fundcode" label="基金代码" width="180"></el-table-column>
      <el-table-column prop="networth" label="净值"></el-table-column>
      <el-table-column prop="date" label="净值日期"></el-table-column>
      <el-table-column prop="gszzl" label="估值"></el-table-column>
      <el-table-column prop="dwjz" label="单位净值"></el-table-column>
      <el-table-column prop="buy" label="推荐买入"></el-table-column>
      <el-table-column prop="hold" label="当前持有"></el-table-column>
      <el-table-column prop="budgetrevenue" label="今日预算收益"></el-table-column>
      <el-table-column prop="earningstoday" label="今日收益"></el-table-column>
      <el-table-column prop="progressiveincome" label="累计收益"></el-table-column>
      <el-table-column prop="rateofreturn" label="累计收益率"></el-table-column>
    </el-table>
    <el-button
      style="margin-top:10px;float:right"
      type="primary"
      @click="dialogFormVisible=true"
      id="determine"
    >添加基金</el-button>
    <el-dialog title="添加基金" :visible.sync="dialogFormVisible">
      <el-form :model="up">
        <el-form-item label="基金代码" :label-width="formLabelWidth">
          <el-input
            style="width:300px;"
            placeholder="请输入密码"
            v-model="add_fundcode"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false" id="cancel">取 消</el-button>
        <el-button type="primary" @click="addfund()" id="determine">确定添加</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      tableData: [],
      market:[],
      add_fundcode: "",
      dialogFormVisible: false
    };
  },
  mounted: function() {
    this.convert();
  },
  methods: {
    convert: function() {
      axios.get("api/getoptionalfund").then(res => {
        this.tableData = res.data["list"];
      });
      axios.get("api/getmarket").then(res => {
        this.market = res.data["stock"];
      });
    },
    addfund() {
      axios
        .post("api/addfund", {
          add_fundcode: this.add_fundcode
        })
        .then(res => {
          this.$message({
            message: res.data["message"],
            type: "success"
          });
          this.convert();
          this.dialogFormVisible = false
        });
    },
    // 这是一个定时器
    timer() {
      return setTimeout(() => {
        this.convert();
      }, 5000);
    }
  },
  watch: {
    list() {
      this.timer();
    }
  },
  destroyed() {
    clearTimeout(this.timer);
  }
};
</script>