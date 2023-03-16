from googleapiclient.discovery import build
from datetime import datetime 
import pandas as pd

youTubeApiKey="AIzaSyB8InT9kdSEBBSPBUApvqGtZ4sAoJTxJ7w"

youtube = build('youtube','v3', developerKey=youTubeApiKey)

playlistId = 'PL5TJqBvpXQv6SSsEgQrNwpOLTupXPuiMQ' #lista do link
playlistName = 'Dicas de Pandas'
nextPage_token = None

playlist_videos = []

while True:
  res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults=50, pageToken=nextPage_token).execute()
  playlist_videos += res['items']
  
  nextPage_token = res.get('nestPageToken')

  if nextPage_token is None:
    break

#print("Número total de vídeos na Playlist ", len(playlist_videos))

videos_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], playlist_videos))
#print('\n'.join(map(str, videos_ids)))

stats = []

for video_id in videos_ids:
  res = youtube.videos().list(part='statistics', id=video_id).execute()
  stats += res['items']

#print(stats)

videos_title = list(map(lambda x: x['snippet']['title'], playlist_videos))
url_thumbnails = list(map(lambda x: x['snippet']['thumbnails']['high']['url'], playlist_videos))
published_date = list(map(lambda x: str(x['snippet']['publishedAt']), playlist_videos)) #conversion from ISO8601 date format
video_description = list(map(lambda x: x['snippet']['description'], playlist_videos))
videoid = list(map(lambda x: x['snippet']['resourceId']['videoId'], playlist_videos))
liked = list(map(lambda x: int(x['statistics']['likeCount']), stats))
views = list(map(lambda x: int(x['statistics']['viewCount']), stats))
comment = list(map(lambda x: int(x['statistics']['commentCount']), stats))
extraction_date = [str(datetime.now())]*len(videos_ids)

playlist_df = pd.DataFrame({
    'title':videos_title,
    'video_id':videoid,
    'video_description':video_description,
    'published_date':published_date,
    'extraction_date':extraction_date,
    'likes':liked,
    'views':views,
    'comment':comment,
    'thumbnail': url_thumbnails
})

playlist_df.head()

r = ""

y=input("############\nDigite qual a ordem que você deseja: \n1 - views\n2 - Likes\n3 - Comentarios: \n4 - Id dos videos\n############\n")
match y:
    case "1":
        r = "views"
    case "2":
        r = "likes"
    case "3":
        r = "comment"
    case "4":
        r = "video_id"

if (r != "video_id" and y >= "1" and y <= "3"):
    x = playlist_df.sort_values(by=r, ascending=False)
    print(x) #TABELA DOS DADOS
else:
    print(playlist_df) #TABELA DOS DADOS

# colocar alguma formula para exibir (exemplo que mais se repete ou mais curtidos)
#for(i=0; i<vetor.length; i++)
#	{
#	for(int j=0; j<vetor.length; j++)
#		if (vetor[i] == vetor[j])
#		cont++;
#		num = vetor[i];
#		}
#	print(" repeticoes numero " + num + ": " + cont + " vezes");	
#	} 
