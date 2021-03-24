def obterListaMedia(listaOriginal):
    listaMedia = []

    for i in range(1, len(listaOriginal)+1):
        recorte = listaOriginal[:i]
        media = sum(recorte)/len(recorte)
        listaMedia.append(media)
    
    return listaMedia