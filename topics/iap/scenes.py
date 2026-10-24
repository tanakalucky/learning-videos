from engine.draw import Canvas,progress,BLUE,GREEN,RED,GOLD,MUTED
DURATION=78
SCENES=[
(0,9,'IAPは、アプリの入口を守る','Identity-Aware Proxy','URLを知っていても、誰でも入れるわけではありません。\nIAPは「誰がアクセスできるか」を入口で確認します。'),
(9,20,'まず「あなたは誰？」','01  認証 / Authentication','未ログインなら、ブラウザをログイン画面へ案内します。\n認証は、利用者が誰なのかを確かめることです。'),
(20,31,'次に「このアプリへ入れる？」','02  認可 / Authorization','本人確認のあと、IAPがIAMポリシーを確認します。\nログインできることと、アプリへ入れることは別です。'),
(31,43,'許可された人は、アプリへ','例：対象のアプリへのアクセス権があるAさん','IAPのアクセス権があるAさんは、アプリへ進めます。\nユーザーやグループに、対象リソースへの権限を設定します。'),
(43,54,'許可がなければ、入口で拒否','例：ログイン済みでも、アクセス権がないBさん','Bさんも本人確認は済んでいますが、アクセス権がありません。\nIAPが拒否し、この要求はアプリへ届きません。'),
(54,66,'入れたあとも、権限はある','03  アプリ内の業務権限','IAPを通過しても、すべての操作ができるわけではありません。\n「閲覧・編集・承認」などは、アプリ側で制御します。'),
(66,78,'覚えるのは、この3つ','認証 → IAPでの認可 → アプリ内の権限','認証は「誰か」、IAPの認可は「入れるか」。\nアプリ内の権限は「何ができるか」です。')]
def scene_at(t):
 t=max(0,min(DURATION-1/30,t)); return next((i,s) for i,s in enumerate(SCENES) if s[0]<=t<s[1])
def render(t):
 i,s=scene_at(t); start,end,title,tag,sub=s; u=t-start; c=Canvas(); c.frame(i+1,title,tag,sub,t,DURATION)
 if i==0:
  c.person(112,278,'利用者'); c.card(430,235,280,260,'IAP','アプリへの\nアクセスを判断'); c.card(939,265,280,200,'アプリ','保護された入口',GREEN)
  c.arrow(240,352,410,352,progress(u,1,2)); c.arrow(730,352,919,352,progress(u,3,2),GREEN); c.pill(464,432,'誰が入れる？',GOLD)
 elif i==1:
  c.person(105,272,'利用者'); c.card(400,230,330,275,'ログイン','Googleアカウントなど\n本人確認を行う'); c.arrow(235,342,380,342,progress(u,1,2))
  c.card(885,265,325,205,'本人確認','利用者のIDがわかる',GREEN)
  if u>4: c.arrow(750,342,865,342,progress(u,4,2),GREEN)
  if u>7: c.pill(449,434,'認証が完了',GREEN)
 elif i==2:
  c.card(65,240,310,238,'認証済み','Aさんです\nBさんです',GREEN); c.card(475,220,330,300,'IAPの認可','IAMポリシーを確認\nこの人は入れる？'); c.arrow(395,355,455,355,progress(u,1,2))
  c.card(895,240,320,238,'アクセス権','対象リソースへの\n許可があるか',GOLD)
  if u>4: c.arrow(875,355,825,355,progress(u,4,2),GOLD)
  c.text(640,459,'ログイン済み ≠ 入場許可',24,GOLD,'mt')
 elif i in (3,4):
  allowed=i==3; col=GREEN if allowed else RED
  c.person(110,267,'Aさん' if allowed else 'Bさん',col); c.card(405,245,270,220,'IAP','本人確認  済み\nアクセス権を確認'); c.card(920,245,265,220,'アプリ','社内ポータル',GREEN if allowed else MUTED)
  c.arrow(235,343,385,343,progress(u,.5,1.8),col)
  if u>3: c.pill(422,408,'許可' if allowed else '拒否',col)
  if allowed:
   if u>4: c.arrow(695,343,900,343,progress(u,4,2),GREEN)
   if u>6: c.pill(959,408,'アクセス成功',GREEN)
   c.text(640,524,'例：IAP-secured Web App User ロール',24,MUTED,'mt')
  else:
   if u>4: c.text(784,319,'×',52,RED,'mt'); c.text(784,390,'ここで停止',24,RED,'mt')
   c.text(640,524,'同じログイン済みでも、結果は違う',25,GOLD,'mt')
 elif i==5:
  c.card(60,260,255,210,'IAPを通過','アプリへ入れる',GREEN); c.arrow(335,365,465,365,progress(u,1,2),GREEN); c.box(485,214,730,338,GREEN); c.text(515,237,'アプリ側のルール（例）',30,GREEN)
  for x,title,body,col in [(515,'閲覧','許可',GREEN),(745,'編集','権限が必要',GOLD),(975,'承認','権限が必要',GOLD)]: c.card(x,310,200,202,title,body,col)
 else:
  for j,(a,b,col) in enumerate([('認証','誰か',BLUE),('IAPの認可','入れるか',GREEN),('アプリ内権限','何ができるか',GOLD)]):
   x=60+j*415; c.card(x,222,330,180,a,b,col)
   if j<2: c.arrow(x+345,312,x+395,312,progress(u,j+1,1),col)
  c.box(60,439,1160,110); c.text(88,455,'Cloud Runでは、サービスへ直接IAPを設定できます。',28); c.text(88,500,'ロードバランサーが常に必要なわけではありません。',26,MUTED); c.text(640,560,'Google Cloud 公式資料に基づく模式図 / 2026-10-24確認',18,MUTED,'mt')
 return c.im
