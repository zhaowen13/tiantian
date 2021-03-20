<template>
  <mytable :data="set_data"></mytable>
</template>
<script>
import mytable from "@/components/table";
export default {
  components: { mytable },
  setup() {
    const set_data = {
      name: "股票",
      heads: [
        {
          prop: "name",
          label: "股票名称",
        },
        {
          prop: "code",
          label: "股票代码",
        },
        {
          prop: "newest",
          label: "最新价",
        },
        {
          prop: "quote_change",
          label: "涨跌幅",
        },
      ],
      del_url: "",
      add_url: "",
      get_url: "getmarket",
    };
    return {
      set_data,
    };
  },
};
</script>
