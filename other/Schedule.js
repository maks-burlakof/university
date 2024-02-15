// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: calendar-alt;
let groupNum = "122402";
let subgroupNum = 1;

async function getPairs() {
  let data = await new Request("https://iis.bsuir.by/api/v1/schedule?studentGroup="+groupNum).loadJSON();
  return data.schedules;
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

  let today = new Date();
  let df = new DateFormatter();
  df.locale = "ru";
  df.dateFormat = "EEEE";
  let todayWeekDay = df.string(today);
  df.dateFormat = "E, d MMM";
  let todayString = df.string(today);
  
  let currentWeekDay = todayWeekDay[0].toUpperCase() + todayWeekDay.slice(1);
  let currentWeekNum = await getWeekNum();
  let pairs = await getPairs();
  
  let headerStack = widget.addStack();
  headerStack.layoutHorizontally();
  let headerTodayText = headerStack.addText(todayString);
  headerStack.addSpacer();
  headerStack.addText(groupNum);
  headerTodayText.font = Font.headline();
  widget.addSpacer(10);
  
  let pairColors = {
    "ПЗ": "#ff0000",
    "ЛК": "#7cfc00",
    "ЛР": "#fdda0d",
  }
  
  let pairsCount = 0;
  pairs[currentWeekDay].forEach(pair => {
    if (pair.weekNumber.includes(currentWeekNum)&& ((pair.numSubgroup === 0 || pair.numSubgroup === subgroupNum) || subgroupNum === 0)) {
      pairsCount++;
      let pairMainStack = widget.addStack();
      // Time
      let pairLeftStack = pairMainStack.addStack();
      pairLeftStack.layoutVertically();
      pairLeftStack.setPadding(0,0,0,10);
      let startTime = pairLeftStack.addText(pair.startLessonTime);
      startTime.font = Font.regularMonospacedSystemFont(15);
      endTime = pairLeftStack.addText(pair.endLessonTime);
      endTime.font = Font.regularMonospacedSystemFont(13);
      endTime.textOpacity = 0.7;
      // Line
      let pairCenterStack = pairMainStack.addStack();
      pairCenterStack.layoutVertically();
      pairCenterStack.setPadding(20,5,12,3)
      pairCenterStack.backgroundColor = new Color(pairColors[pair.lessonTypeAbbrev]);
      pairCenterStack.cornerRadius = 4;
      // Subject info
      let pairRightStack = pairMainStack.addStack();
      pairRightStack.layoutVertically();
      pairRightStack.setPadding(0,10,0,0);
      let subjectText = pairRightStack.addText(pair.subject + (pair.numSubgroup ? ("  👤" + pair.numSubgroup) : ""));
      subjectText.font = Font.boldSystemFont(15);
      let auditoriesText = pairRightStack.addText(pair.auditories.join(", "));
      auditoriesText.font = Font.regularSystemFont(13);
      auditoriesText.textOpacity = 0.7;
      
      widget.addSpacer(5);
    }
  })
  
  let paddingsBottom = {
    0: 300,
    1: 260,
    2: 220,
    3: 180,
    4: 150,
    5: 110,
    6: 80,
  }
  widget.setPadding(20,20,paddingsBottom[pairsCount],20);
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