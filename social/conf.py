def cherry_conf(root):
    return {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': root
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './assets'
        }
    }