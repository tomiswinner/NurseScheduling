'use stirct';

function makeTable(dateData,memData){
  const TId = document.getElementById('workingtable');
  const rows =[];
  const table = document.createElement("table");

  for(i = 0; i< dateData.length + 1; i++){ //必要な列は日付+ 1(= へっだ)
    rows.push(table.insertRow(-1)); //行追加
    for(j = 0; j < memData.length + 1; j++){ //同上
      cell = rows[i].insertCell(-1);
      // if(i==0&&j>=1){
      //   cell.appendChild(document.createTextNode(memData[j]));
      // }
      // if(i>=0&&j==0){
      //   cell.appendChild(document.createTextNode(dateData[i]));
      // }
    }
    TId.appendChild(table);
  }
}

