
// Nice Timestamp
// TS: 20240820081033
// returns:  "20 Aug 2024, 08:10:33"
function TimeStamp(timestamp) {

    const s = String(timestamp);

    const year   = s.slice(0, 4);
    const month  = s.slice(4, 6);
    const day    = s.slice(6, 8);
    const hour   = s.slice(8, 10);
    const minute = s.slice(10, 12);
    const second = s.slice(12, 14);

    const date = new Date(
        Number(year),
        Number(month) - 1,
        Number(day),
        Number(hour),
        Number(minute),
        Number(second)
    );

    return date.toLocaleString("en-AU", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
    });
}



// Nice Date
// TS: 20240820081033
// returns:  "20 Aug 2024, 08:10:33"
function NiceDate(timestamp) {

    try {
        return TimeStamp(timestamp).split(",")[0]
    } catch(error) {
        return ""
    }
   
}

function NiceTS(timestamp) {

    try {
        return TimeStamp(timestamp)
    } catch(error) {
        return ""
    }
   
}
