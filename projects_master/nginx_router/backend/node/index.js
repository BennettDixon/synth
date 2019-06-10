const express = require("express");

const app = express();

app.get("/api/v1", (req, res) => {
  res.send(JSON.stringify({ value: "Synth is running!!!" }));
});

app.listen(5005, () => {
  console.log("Express app listening on port 5005");
});
