/**
 *   获取年月日
 *   @returns {string}  yyyy-mm-dd
 */

export function getDate() {
    const date = new Date()
    return date.getFullYear() + '-' + addZero(date.getMonth() + 1) + '-' + addZero(date.getDate())
}

export function getWeekDay() {
    const date = new Date()
    var weeks = new Array("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六");
    var week = weeks[date.getDay()];
    return week
}

/**
 *   获取时分秒
 *   @returns {string}  hh:mm:ss
 */

export function getTime() {
    const date = new Date()
    return addZero(date.getHours()) + ':' + addZero(date.getMinutes()) + ':' + addZero(date.getSeconds())
}

/**
 *   如果小于10 ，就补0
 *   @param {string} date
 *   @returns {string}  date
 */
function addZero(item) {
    return item > 9 ? item : '0' + item
}