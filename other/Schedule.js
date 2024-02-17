// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: calendar-alt;
// User config
let groupNum = "122402";
let subgroupNum = 1;

let today = new Date();
let df = new DateFormatter();
df.locale = "ru";

async function getDatePairs() {
  let data = await new Request("https://iis.bsuir.by/api/v1/schedule?studentGroup="+groupNum).loadJSON();
  
  let date = new Date();
  df.dateFormat = "EEEE";
  for (let i = 0; i < 7; i++) {
    date.setDate(today.getDate() + i);
    let weekDay = df.string(date);
    weekDay = weekDay[0].toUpperCase() + weekDay.slice(1);
    if (weekDay in data.schedules) {
      return [date, data.schedules[weekDay]];
    }
  }
  return [null, null]
}

async function getWeekNum() {
  let data = await new Request("https://iis.bsuir.by/api/v1/schedule/current-week").loadString();
  return parseInt(data);
}

async function createWidget() {
  let widget = new ListWidget();
  widget.addAccessoryWidgetBackground = true;
  widget.addSpacer(1);
  //widget.url = "";
  //widget.backgroundColor = new Color("#000000");
  
  let currentWeekNum = await getWeekNum();
  let [date, pairs] = await getDatePairs();
  
  // Header
  df.dateFormat = "E, d MMM";
  let dateString = df.string(date);
  let headerStack = widget.addStack();
  headerStack.layoutHorizontally();
  let headerTodayText = headerStack.addText(dateString);
  headerStack.addSpacer();
  headerStack.addText(groupNum);
  headerTodayText.font = Font.headline();
  widget.addSpacer(15);
  
  let pairColors = {
    "ПЗ": "#ff3b30",
    "ЛК": "#34c759",
    "ЛР": "#ffcc00",
  }
  
  let pairExpiredColors = {
    "ПЗ": ["#f6bbbb", "#8e302c"],
    "ЛК": ["#b9e5c7", "#26773b"],
    "ЛР": ["#f6e6ac", "#8e7914"],
  }
  
  let pairsCount = 0;
  let pairsAreOver = true;
  
  pairs.forEach(pair => {
    if (pair.weekNumber.includes(currentWeekNum)&& ((pair.numSubgroup === 0 || pair.numSubgroup === subgroupNum) || subgroupNum === 0)) {
      pairsCount++;
      let pairMainStack = widget.addStack();
      let pairLeftStack = pairMainStack.addStack();
      pairLeftStack.layoutVertically();
      pairLeftStack.setPadding(0,0,0,10);
      let pairCenterStack = pairMainStack.addStack();
      pairCenterStack.layoutVertically();
      pairCenterStack.setPadding(32,5,0,3);
      let pairRightStack = pairMainStack.addStack();
      pairRightStack.layoutVertically();
      pairRightStack.setPadding(0,10,0,0);
      
      // Time
      let startTimeText = pairLeftStack.addText(pair.startLessonTime);
      startTimeText.font = Font.regularMonospacedSystemFont(15);
      endTimeText = pairLeftStack.addText(pair.endLessonTime);
      endTimeText.font = Font.regularMonospacedSystemFont(13);
      endTimeText.textOpacity = 0.7;
      
      // Subject
      let subjectText = pairRightStack.addText(pair.subject + (pair.numSubgroup ? ("  👤" + pair.numSubgroup) : ""));
      subjectText.font = Font.boldSystemFont(15);
      let auditoriesText = pairRightStack.addText(pair.auditories.join(", "));
      auditoriesText.font = Font.regularSystemFont(13);
      auditoriesText.textOpacity = 0.7;
      
      // Line
      pairCenterStack.backgroundColor = new Color(pairColors[pair.lessonTypeAbbrev]);
      
      let pairStartTime = new Date();
      pairStartTime.setHours(...pair.startLessonTime.split(":").map(Number),0,0);
      let pairEndTime = new Date();
      pairEndTime.setHours(...pair.endLessonTime.split(":").map(Number),0,0);
      
      if (today < pairStartTime && today < pairEndTime) {
        pairsAreOver = false;
      } 
      else if (today > pairStartTime && today < pairEndTime) {
        pairsAreOver = false;
        subjectText.textOpacity = 0.7;
        startTimeText.textOpacity = 0.7;
        let lineHeight = 32 * Math.floor((pairEndTime - today) / (1000*60)) / 80;
        pairCenterStack.setPadding([32, 24, 16, 8].reduce((prev, curr) => (Math.abs(curr - lineHeight) < Math.abs(prev - lineHeight) ? curr : prev)), 5, 0, 3);
      }
      else if (today > pairStartTime && today > pairEndTime) { 
        pairCenterStack.backgroundColor = Color.dynamic(new Color(pairExpiredColors[pair.lessonTypeAbbrev][0]), new Color(pairExpiredColors[pair.lessonTypeAbbrev][1]));
      }
      pairCenterStack.cornerRadius = 4;
      
      widget.addSpacer(5);
    }
  })
  
  // widgetPaddings
  let paddingsBottom = {
    0: 290,
    1: 255,
    2: 220,
    3: 185,
    4: 150,
    5: 115,
    6: 80,
    7: 45,
  }
  widget.setPadding(20,20,paddingsBottom[pairsCount],20);
  
  // nextRefreshDate
  let nextRefreshDate = new Date();
  if (pairsAreOver === true) {
    nextRefreshDate.setHours(0, 0, 0, 0);
    nextRefreshDate.setDate(nextRefreshDate.getDate() + 1);
  } else {
    nextRefreshDate.setMinutes(today.getMinutes() + 20);
  }
  widget.refreshAfterDate = nextRefreshDate;

  return widget;
}

async function renderWidget() {
  let widget = await createWidget();
  if (config.runsInWidget) {
    Script.setWidget(widget);
  } else {
    widget.presentLarge();
  }
  Script.complete();
}

await renderWidget();