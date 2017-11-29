#!/usr/bin/Rscript
setwd("C:/Relatorio")
###Load Files
Ffogo=list.files(pattern ='B\\d*.csv' )
Fsoja=list.files(pattern ='S\\d*.csv' )
Fcont=list.files(pattern ='C\\d*.csv' )



NetworkError=''
NetworkErrorNumber=0
###Load Lib
###
library(dplyr)
library(ggplot2)

#Crerrega um arquivo ou mais de um, dentro de um dataframe 
#
createTables<-function(files){
  if(length(files)==1){
    return(read.csv(files))
  }else{
    dataFrame=read.csv(files[1])
    for (f in 2:length(files)){
      tmpFile=read.csv(files[f])
      dataFrame=bind_rows(normalizeDataFrame(dataFrame), normalizeDataFrame(tmpFile))
    }
    return (dataFrame)
   }
}

normalizeDataFrame<-function(dataFrame){
  return(data.frame(lapply(dataFrame, as.character), stringsAsFactors=FALSE))
}

#Obtem os dados importante do dataframe
#
editTables<-function(file,torre){
  if(identical(file,character(0))){
    assign("NetworkError",paste(NetworkError,'<p>The ',torre,' is offine!.</p>',sep = '') , envir = .GlobalEnv)
    assign('NetworkErrorNumber', NetworkErrorNumber+1, envir = .GlobalEnv)
    finalFile=NULL
  }else{
    dataTabe=createTables(file)
    finalFile=dataTabe
    finalFile$Torre=torre
  }
  return(finalFile)
}


###Cria dataframe das torre com mes dia e ano
torres=plyr::rbind.fill(editTables(Fcont,'Control'),editTables(Fsoja,'Soy'),editTables(Ffogo,'Burned'))
torres$Ano=format(as.Date(torres$Date...Time,"%d.%m.%Y"),'%Y')
torres$Mes=format(as.Date(torres$Date...Time,"%d.%m.%Y"),'%m')
torres$Dia=format(as.Date(torres$Date...Time,"%d.%m.%Y"),'%d')
torres$data=as.Date(torres$Date...Time,"%d.%m.%Y")
torres$cont=1
torres$hora=as.numeric(as.character(substr(torres$Date...Time,12,13)))
##Calcula a frequecia das torres


if(NetworkErrorNumber<3){
  lif=doBy::summaryBy(cont~data+hora+Torre,torres,keep.names=T,FUN=sum)
  lif2=subset(lif,data>Sys.Date()-10)
  f1=ggplot() +   
    geom_tile(data=lif2, aes(x=hora, y=data, fill=as.factor(cont)), colour="white", size=0.05)+
    facet_grid(~Torre)+
    theme_bw()+
    labs(list(x = "Hour", y = "Data"),size=2)+
    theme(legend.title=element_blank(),
          axis.title.x=element_text(size=12,vjust=0.4),
          strip.text.y = element_text(angle = 90))
  
  
  ggsave(filename = "gf1.jpg", plot = f1,
         width = 15, height = 8, units =  "cm", dpi = 150)
  
  
  #graficos de dados de meteorologicos
  
  df=subset(torres,data>Sys.Date()-5,select = c(Torre,Date...Time,H,LE,C,t_air,rh_air))
  df2=plyr::mutate(df,
        H=ifelse(H<0|H>500,NA,H),
        LE=ifelse(LE<0|LE>500,NA,LE),
        C=ifelse(C<(-50)|C>100,NA,C),
        rh_air=ifelse(rh_air>100,100,rh_air))
  
  
  
  df3=reshape2::melt(df2,id=c("Torre","Date...Time"))
  
  df3$var=factor(df3$variable,labels = c("Sensible heat (W/m²)","Latent heat (W/m²)",
                                         "CO2 (μmol m²/s)",
                                         "Air temperature (Celsius)",
                                         "Relative humidity (%)"))
  df3$data=lubridate::ymd_hm(paste(as.Date(df3$Date...Time,"%d.%m.%Y"),
                            substr(df3$Date...Time,12,16),sep = " "))
  
  
  
  f2=ggplot(df3,aes(x=data, y=value, colour=as.factor(Torre)))+
    geom_point(alpha=.6)+
    geom_smooth(aes(x=data, y=value, colour=as.factor(Torre)),
                method = 'loess',se=F,span=0.1,lwd=0.4)+
    facet_wrap(~var,scale="free_y",ncol=1)+
    theme_bw(base_size = 14)+
    labs(list(x = "Date", y = NULL),size=2)+
    theme(legend.title=element_blank(),
          axis.title.x=element_text(size=12,vjust=0.4),
          strip.text.y = element_text(angle = 90)
          #legend.position = c(.7,.1)
          )

  ggsave(filename = "gf2.jpg", plot = f2,
         width = 15, height = 8*5, units =  "cm", dpi = 150)

# Chuva$data=as.Date(Chuva$TIMESTAMP,"%Y-%m-%d")
# Chuva$time=lubridate::ymd_hms(Chuva$TIMESTAMP)
# 
# f3=ggplot(Chuva,aes(x=time, y=Batt_Min))+
#     geom_point(alpha=.6)+
#     theme_bw(base_size = 14)+
#     labs(list(x = "Date", y = NULL),size=2)
#     theme(legend=NULL)
#       legend.title=element_blank(),
#          axis.title.x=element_text(size=12,vjust=0.4),
#          strip.text.y = element_text(angle = 90)
#           legend.position = c(.7,.1)
#     )
#   
#   ggsave(filename = "gf3.jpg", plot = f3,
#          width = 15, height = 8, units =  "cm", dpi = 150)
#   
#   
#   
  
  
  
  if(NetworkErrorNumber>0){
    writeChar(paste('<h3>Error connecting to the towers</h3>',NetworkError),'erroSys.html',eos=NULL) 
  }else{
    writeChar(paste('<p></p>'),'erroSys.html',eos=NULL) 
  }
  writeChar(paste('{"body":"body.html", "error":false}'),'openFileHTML.json',eos=NULL)
}else{
  writeChar(paste('{"body":"notTorre.html","error":true}'),'openFileHTML.json',eos=NULL)
}

writeChar(paste(Sys.time(),Sys.timezone()),'reportTime',eos=NULL) 
