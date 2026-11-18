"""EcoFlow DELTA 2 live reserve using its signed read-only Open API."""
import hashlib,hmac,json,os,secrets,time,urllib.parse,urllib.request
from serve import page
INTERVAL=60
def fetch_quota(o):
    access=os.environ["ECOFLOW_ACCESS_KEY"];secret=os.environ["ECOFLOW_SECRET_KEY"];serial=os.environ["ECOFLOW_SERIAL"]
    origin=o.get("origin","https://api.ecoflow.com")
    if origin not in ("https://api.ecoflow.com","https://api-e.ecoflow.com","https://api-a.ecoflow.com"):raise ValueError("Select an EcoFlow API region")
    nonce=str(secrets.randbelow(900000)+100000);stamp=str(int(time.time()*1000))
    fields="sn="+serial+"&accessKey="+access+"&nonce="+nonce+"&timestamp="+stamp
    signature=hmac.new(secret.encode(),fields.encode(),hashlib.sha256).hexdigest()
    request=urllib.request.Request(origin+"/iot-open/sign/device/quota/all?"+urllib.parse.urlencode({"sn":serial}),headers={"accessKey":access,"nonce":nonce,"timestamp":stamp,"sign":signature})
    with urllib.request.urlopen(request,timeout=8) as r:return json.load(r)
def parse(payload,reserve):
    if str(payload.get("code"))!="0":raise ValueError("EcoFlow did not return success")
    data=payload["data"];level=float(data["pd.soc"])
    if not 0<=level<=100 or not 0<=reserve<=100:raise ValueError("Invalid charge percentage")
    output=float(data["pd.wattsOutSum"]);incoming=float(data["pd.wattsInSum"])
    raw=data.get("pd.remainTime");remaining=float(raw) if raw is not None else None
    minutes=(abs(remaining)*max(0,level-reserve)/level if remaining is not None and remaining<0 and level>0 else 0 if level<=reserve else None)
    return level,output,incoming,minutes
def snapshot(o,m):
    reserve=float(o.get("reserve_percent",20));level,out,inc,minutes=parse(fetch_quota(o),reserve)
    budget="--" if minutes is None else f"{int(minutes)//60}h{int(minutes)%60:02d}"
    return dict(state="DELTA 2 / live",key=str(level<=reserve),alert=level<=reserve,pages=[
      page("STATION SOC",f"{level:g}%",f"Output {out:g} W / in {inc:g} W",f"Keep {reserve:g}% in reserve",fraction=level/100),
      page("TO RESERVE",budget,"At the current net load","-- while charge time unknown",fraction=max(0,(level-reserve)/max(1,100-reserve))),
      page("LOAD",f"{out:g}W",f"Input {inc:g} W","AC + DC reported by station")])
