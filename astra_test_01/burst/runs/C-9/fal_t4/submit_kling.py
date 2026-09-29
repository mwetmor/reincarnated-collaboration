import fal_client, json, sys, time
ep=sys.argv[1]; tag=sys.argv[2]
img=fal_client.upload_file('knight_E_ref_1024.png'); vid=fal_client.upload_file('knight_carrywalk_E_drive.mp4')
args={"image_url":img,"video_url":vid,"character_orientation":"video","keep_original_sound":False,
      "prompt":"A knight in plate armour and a blue heraldic tabard walks steadily in place, holding his pollaxe upright in his right hand. The background stays flat pure green. The camera does not move."}
h=fal_client.submit(ep, arguments=args)
json.dump({'endpoint':ep,'request_id':h.request_id,'args':args},open(f'kling_{tag}_request.json','w'),indent=1)
print('submitted',h.request_id, flush=True)
t0=time.time()
res=h.get()
json.dump({'result':res,'elapsed_s':round(time.time()-t0,1)},open(f'kling_{tag}_result.json','w'),indent=1)
print('done',round(time.time()-t0,1),'s', json.dumps(res)[:300], flush=True)
