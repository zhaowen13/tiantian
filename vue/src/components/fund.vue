<template>
  <mytable :data="set_data"></mytable>
</template>
<script>
import mytable from "@/components/table";
export default {
  components: { mytable },
  setup() {
    const set_data = {
      name: "基金",
      heads: [
        {
          prop: "fundcode",
          label: "基金代码",
        },
        {
          prop: "name",
          label: "基金名称",
        },
        {
          prop: "networth",
          label: "净值",
        },
        {
          prop: "date",
          label: "净值日期",
        },
        {
          prop: "quote_change",
          label: "涨跌幅",
        },
        {
          prop: "dwjz",
          label: "单位净值",
        },
        {
          prop: "buy",
          label: "推荐买入",
        },
        {
          prop: "hold",
          label: "当前持有",
        },
        {
          prop: "budgetrevenue",
          label: "今日预算收益",
        },
        {
          prop: "earningstoday",
          label: "今日收益",
        },
        {
          prop: "progressiveincome",
          label: "累计收益",
        },
        {
          prop: "rateofreturn",
          label: "累计收益率",
        }
      ],
      del_url: "",
      add_url: "",
      get_url: "getoptionalfund",
    };
    return {
      set_data,
    };
  },
};
</script>