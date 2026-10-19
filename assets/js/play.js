(function(){
  var jobs=["RTP media","SDP offer and answer","SIP session setup","A price stays confirm"];
  var want=["SIP session setup","SDP offer and answer","RTP media","A price stays confirm"];
  var list=document.getElementById("order");
  if(!list) return;
  jobs.forEach(function(job){
    var li=document.createElement("li");
    li.textContent=job;
    li.draggable=true;
    li.dataset.job=job;
    li.style.padding="8px";
    li.style.margin="6px 0";
    li.style.border="2px solid #0f766e";
    li.style.borderRadius="12px";
    li.addEventListener("dragstart",function(){li.classList.add("dragging");});
    li.addEventListener("dragend",function(){li.classList.remove("dragging");});
    list.appendChild(li);
  });
  list.addEventListener("dragover",function(ev){
    ev.preventDefault();
    var dragging=list.querySelector(".dragging");
    var after=[].slice.call(list.children).find(function(child){
      var box=child.getBoundingClientRect();
      return ev.clientY < box.top + box.height/2;
    });
    if(!dragging) return;
    if(after) list.insertBefore(dragging, after); else list.appendChild(dragging);
  });
  document.getElementById("check-order").addEventListener("click",function(){
    var got=[].map.call(list.children,function(li){return li.dataset.job;});
    var ok=got.every(function(item,i){return item===want[i];});
    document.getElementById("play-note").textContent=ok?"That order matches the study habit.":"Not yet. SIP session setup, then SDP, then RTP. A price is a different object.";
  });
})();
(function(){
  var form=document.getElementById("sim-form");
  if(!form) return;
  var node="INVITE";
  document.querySelectorAll("[data-sim-node]").forEach(function(btn){
    btn.addEventListener("click",function(){
      node=btn.getAttribute("data-sim-node");
      document.querySelectorAll("[data-sim-node]").forEach(function(el){el.setAttribute("aria-pressed", el===btn?"true":"false");});
    });
  });
  form.addEventListener("submit",function(event){
    event.preventDefault();
    var uri=document.getElementById("sim-uri").value.trim()||"sip:example.test";
    var digit=document.getElementById("sim-dtmf").value.trim()||"—";
    var branch=document.getElementById("sim-branch").value;
    var branchLine=branch==="queue"?"IVR branch: queue. Simulated. No agent was offered a call.":branch==="voicemail"?"IVR branch: voicemail. Simulated. No mailbox was opened.":"IVR branch: hang up. Simulated BYE. No carrier was signaled.";
    var step=node==="INVITE"?"Simulated INVITE to "+uri+". Next sketch: 100 Trying, then 180 Ringing. Not run on a network.":node==="180"?"Simulated 180 Ringing for "+uri+". Media is not flowing yet.":node==="200"?"Simulated 200 OK for "+uri+". The sketch then expects ACK, then RTP. Not run on a network.":node==="ACK"?"Simulated ACK. The teaching sketch would start RTP after this. No packets were sent.":"Simulated BYE for "+uri+". The sketch ends the dialog. Not run on a network.";
    document.getElementById("sim-out").textContent=step+"\nDTMF digit on the form: "+digit+" (not sent).\n"+branchLine;
  });
})();
