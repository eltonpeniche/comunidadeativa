def site_info(request):
    return {
        'endereco': {
            'logradouro': 'Av. Presidente Vargas',
            'numero': '814',
            'bairro': 'Campina',
            'cidade': 'Belém',
            'uf': 'Pará',
            'cep': '66017-060',
        },
        'redes_sociais': {
            'twitter': 'https://www.twitter.com/exemplo',
            'facebook': 'https://www.facebook.com/exemplo',
            'instagram': 'https://www.instagram.com/exemplo',
            'linkedin': 'https://www.linkedin.com/exemplo',
        },
        'contato':{
            'email':'comunidadeativa@email.com',
            'telefone':'55 995548855'
        }
    }