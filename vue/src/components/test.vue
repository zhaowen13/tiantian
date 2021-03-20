 <template>
  <el-table :data="tableData" style="width: 100%" :cell-style="cellStyle">
    <el-table-column prop="date" label="日期" width="180"> </el-table-column>
    <el-table-column prop="name" label="姓名" width="180"> </el-table-column>
    <el-table-column prop="address" label="地址"> </el-table-column>
  </el-table>
</template>

<script>
export default {
   setup(){
     const tableData=[{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1517 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1519 弄'
          }, {
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1516 弄'
          }];
     return{
       tableData,
       cellStyle,
     };
     function cellStyle({row, column}) {
      let cellStyle;
      if ( row.name.indexOf('王') ) {
        cellStyle = "color: red;font-weight:bold";
      } else {
        cellStyle = "color: green;font-weight:bold";
      }
      if (column.label == "估值" || column.label=="日期") return cellStyle;
    }
    }
   };
</script>