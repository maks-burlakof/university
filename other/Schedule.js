// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: calendar-alt;
// User config
let groupNum = "122402";
let subgroupNum = 1;

// Color config
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

let today = new Date();
let pairsCurrentCount = 0, pairsNextCount = 0;
let df = new DateFormatter();
df.locale = "ru";

async function getPairs(widget) {
  let pairsData = await getPairsData();
  let weekNum = await getWeekNum();
  let date = new Date(today);
  let nextRefreshDate = null;
  let response = {
    "previous": {
      "date": null,
      "weekNum": null,
      "pairs": null,
    },
    "current": {
      "date": null,
      "weekNum": null,
      "pairs": null,
    },
    "next": {
      "date": null,
      "weekNum": null,
      "pairs": null,
    },
  }
  
  df.dateFormat = "EEEE";
  for (let i = 0; i < 7; i++) {
    date.setDate(today.getDate() + i);
    let weekDay = df.string(date);
    weekDay = weekDay[0].toUpperCase() + weekDay.slice(1);
    // increase weekNum
    if (weekDay === "Понедельник" && i > 0) {
      weekNum = weekNum < 4 ? weekNum+1 : 1;
    }
    if (weekDay in pairsData) {
      let pairsAreOver = true;
      let pairsCount = 0;
      let pairStartTime = new Date(date);
      let pairEndTime = new Date(date);
      pairsData[weekDay].forEach(pair => {
        if (pair.weekNumber.includes(weekNum) && ((pair.numSubgroup === 0 || pair.numSubgroup === subgroupNum) || subgroupNum === 0) && !["Экзамен", "Консультация"].includes(pair.lessonTypeAbbrev)) {
          pairsCount++;
      pairStartTime.setHours(...pair.startLessonTime.split(":").map(Number),0,0);
      pairEndTime.setHours(...pair.endLessonTime.split(":").map(Number),0,0);
          if (today < pairStartTime && today < pairEndTime) {
            pairsAreOver = false;
            if (nextRefreshDate === null) {
              nextRefreshDate = new Date(pairStartTime);
              nextRefreshDate.setMinutes(pairStartTime.getMinutes() + 20);
            }
          }
          else if (today > pairStartTime && today < pairEndTime) {
            pairsAreOver = false;
            if (nextRefreshDate === null) {
              nextRefreshDate = new Date(pairStartTime);
              nextRefreshDate.setMinutes(today.getMinutes() + 20);
            }
          }
          }
          })
          if (pairsCount > 0 && pairsAreOver === true) {
            response.previous.pairs = pairsData[weekDay];
              response.previous.date = new Date(date);
              response.previous.weekNum = weekNum;
          }
          else if (pairsCount > 0 && pairsAreOver === false) {
            if (response.current.pairs === null) {
              response.current.pairs = pairsData[weekDay];
              response.current.date = new Date(date);
              response.current.weekNum = weekNum;
              pairsCurrentCount = pairsCount;
            }
            else {
              response.next.pairs = pairsData[weekDay];
              response.next.date = new Date(date);
              response.next.weekNum = weekNum;
              pairsNextCount = pairsCount;
              widget.refreshAfterDate = nextRefreshDate;
              return [response, widget];
            }
          }
    }
  }
  return [response, widget];
}

async function getPairsData() {
  let data = await new Request("https://iis.bsuir.by/api/v1/schedule?studentGroup="+groupNum).loadJSON();
  return data.schedules;
}

async function getWeekNum() {
  let data = await new Request("https://iis.bsuir.by/api/v1/schedule/current-week").loadString();
  return parseInt(data);
}

function addTableSchedule(pairs, widget) {
  let stack = widget.addStack();
  stack.layoutVertically();
  stack.spacing = 5;
  pairs.pairs.forEach(pair => {
    if (pair.weekNumber.includes(pairs.weekNum)&& ((pair.numSubgroup === 0 || pair.numSubgroup === subgroupNum) || subgroupNum === 0) && !["Экзамен", "Консультация"].includes(pair.lessonTypeAbbrev)) {
      // main stack
      let pairMainStack = stack.addStack();
      pairMainStack.backgroundColor = Color.dynamic(new Color("#f3f2f8"), new Color("#2c2c2e"));
      pairMainStack.cornerRadius = 9;
      pairMainStack.setPadding(4, 4, 4, 4);
      // left stack
      let pairLeftStack = pairMainStack.addStack();
      pairLeftStack.layoutVertically();
      pairLeftStack.setPadding(2, 7, 2, 10);
      // center stack
      let pairCenterStack = pairMainStack.addStack();
      pairCenterStack.layoutVertically();
      pairCenterStack.cornerRadius = 4;
      let pairCenterStackDown = pairCenterStack.addStack();
      pairCenterStackDown.setPadding(36, 5, 0, 3);
      pairCenterStackDown.cornerRadius = 4;
      // right stack
      let pairRightStack = pairMainStack.addStack();
      pairRightStack.layoutVertically();
      pairRightStack.setPadding(2, 10, 2, 0);
      pairMainStack.addSpacer();
      
      // Time
      let startTimeText = pairLeftStack.addText(pair.startLessonTime);
      startTimeText.font = Font.regularMonospacedSystemFont(15);
      endTimeText = pairLeftStack.addText(pair.endLessonTime);
      endTimeText.font = Font.regularMonospacedSystemFont(13);
      endTimeText.textOpacity = 0.7;
      
      // Subject
      if (pair.auditories.length === 0) {
        pairRightStack.addSpacer(6);
      }
      let subjectText = pairRightStack.addText(pair.subject + (pair.numSubgroup ? ("  👤" + pair.numSubgroup) : ""));
      subjectText.font = Font.boldSystemFont(15);
      if (pair.auditories.length !== 0) {
        let auditoriesText = pairRightStack.addText(pair.auditories.join(", "));
        auditoriesText.font = Font.regularSystemFont(13);
        auditoriesText.textOpacity = 0.7;
      }
      
      // Line
      pairCenterStackDown.backgroundColor = new Color(pairColors[pair.lessonTypeAbbrev]);
      
      let pairStartTime = new Date(pairs.date);
      pairStartTime.setHours(...pair.startLessonTime.split(":").map(Number),0,0);
      let pairEndTime = new Date(pairs.date);
      pairEndTime.setHours(...pair.endLessonTime.split(":").map(Number),0,0);
      
      // pair not started
      if (today < pairStartTime && today < pairEndTime) {
      }
      // pair is started
      else if (today > pairStartTime && today < pairEndTime) {
        pairCenterStack.backgroundColor = Color.dynamic(new Color(pairExpiredColors[pair.lessonTypeAbbrev][0]), new Color(pairExpiredColors[pair.lessonTypeAbbrev][1]));
        let lineHeight = 32 * Math.floor((pairEndTime - today) / (1000*60)) / 80;
        lineHeight = [36, 27, 18, 9].reduce((prev, curr) => (Math.abs(curr - lineHeight) < Math.abs(prev - lineHeight) ? curr : prev));
        pairCenterStackDown.setPadding(lineHeight, 5, 0, 3);
        pairCenterStack.setPadding(36 - lineHeight, 0, 0, 0);
      }
      // pair is over
      else if (today > pairStartTime && today > pairEndTime) {
        subjectText.textOpacity = 0.7;
        startTimeText.textOpacity = 0.7;
        pairCenterStackDown.backgroundColor = Color.dynamic(new Color(pairExpiredColors[pair.lessonTypeAbbrev][0]), new Color(pairExpiredColors[pair.lessonTypeAbbrev][1]));
      }
    }
  })
}

function addInlineSchedule(pairs, widget) {
  function addSubStack() {
    let subStack = stackMain.addStack();
    subStack.layoutHorizontally();
    subStack.spacing = 5;
    return subStack;
  }
  let stackMain = widget.addStack();
  stackMain.layoutVertically();
  stackMain.spacing = 5;
  let stackNum = 1, sizeBusy = 0, sizeRequired = 0;
  let stack = addSubStack();
  pairs.pairs.forEach(pair => {
    if (pair.weekNumber.includes(pairs.weekNum)&& ((pair.numSubgroup === 0 || pair.numSubgroup === subgroupNum) || subgroupNum === 0) && !["Экзамен", "Консультация"].includes(pair.lessonTypeAbbrev)) {
      sizeRequired = 8*2 + 15 + 4 + (pair.subject.length * 10) + 2 + 5;
      if (sizeBusy + sizeRequired > 305 && stackNum === 1 && pairsCurrentCount < 4) {
        stack = addSubStack();
        sizeBusy = 0;
        stackNum++;
      }
      
      let pairStack = stack.addStack();
      pairStack.setPadding(5, 8, 5, 8);
      pairStack.backgroundColor = Color.dynamic(new Color("#f3f2f8"), new Color("#2c2c2e"));
      pairStack.cornerRadius = 9;
      let circleStack = pairStack.addStack();
      circleStack.setPadding(15, 15, 0, 0);
      circleStack.cornerRadius = 10;
      circleStack.backgroundColor = new Color(pairColors[pair.lessonTypeAbbrev]);
      if (sizeBusy + sizeRequired <= 305) {
        let textStack = pairStack.addStack();
        textStack.setPadding(-3, 4, 0, 2);
        textStack.addText(pair.subject);
      }
      
      sizeBusy += sizeRequired;
    }
  })
}

async function createWidget() {
  function addDateText(date) {
    df.dateFormat = "E, d MMM";
    let dateText = widget.addText(df.string(date));
    dateText.font = Font.headline();
    widget.addSpacer(10);
  }
  
  let widget = new ListWidget();
  widget.addAccessoryWidgetBackground = true;
  
  let pairs;
  [pairs, widget] = await getPairs(widget);
  
  // current
  if (pairs.current.pairs !== null) {
    addDateText(pairs.current.date);
    addTableSchedule(pairs.current, widget);
  } else {
    widget.addText("Занятий нет");
  }
  // next
  if (pairs.next.pairs !== null && pairsCurrentCount < 5) {
    widget.addSpacer(15);
    addDateText(pairs.next.date);
    if (pairsCurrentCount + pairsNextCount <= 5) {
      addTableSchedule(pairs.next, widget);
    }
    else {
      addInlineSchedule(pairs.next, widget);
    }
  }
  
  widget.addSpacer();

  if (config.runsInWidget) {
    Script.setWidget(widget);
  } else {
    widget.presentLarge();
  }
  Script.complete();
}

await createWidget();