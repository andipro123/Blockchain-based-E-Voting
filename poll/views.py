from django.shortcuts import render,redirect
from . import models
import math
from django.contrib.admin.forms import AuthenticationForm
import time, datetime
from hashlib import sha512, sha256
from .merkleTree import merkleTree
import uuid
from django.conf import settings

def vote(request):
    candidates = models.Candidate.objects.all()
    context = {'candidates': candidates}
    return render(request, 'poll/vote.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('vote')
    else:  
        form = AuthenticationForm()
    return render(request, 'poll/login.html/')

def create(request, pk):
    print(request.user)
    voter = models.Voter.objects.filter(username=request.user.username)[0]
    if request.method == 'POST' and request.user.is_authenticated and not voter.has_voted:
        vote = pk
        lenVoteList = len(models.Vote.objects.all())
        if (lenVoteList > 0):
            block_id = math.floor(lenVoteList / 5) + 1
        else:
            block_id = 1

        priv_key = {'n': int(request.POST.get('privateKey_n')), 'd':int(request.POST.get('privateKey_d'))}
        pub_key = {'n':int(voter.public_key_n), 'e':int(voter.public_key_e)}
        # Create ballot as string vector
        timestamp = datetime.datetime.now().timestamp()
        ballot = "{}|{}".format(vote, timestamp)
        print('\ncasted ballot: {}\n'.format(ballot))
        h = int.from_bytes(sha512(ballot.encode()).digest(), byteorder='big')
        signature = pow(h, priv_key['d'], priv_key['n'])

        hfromSignature = pow(signature, pub_key['e'], pub_key['n'])

        if(hfromSignature == h):
            new_vote = models.Vote(vote=pk)
            new_vote.block_id = block_id
            new_vote.save()
            status = 'Ballot signed successfully'
            error = False
        else:
            status = 'Authentication Error'
            error = True
        context = {
            'ballot': ballot,
            'signature': signature,
            'status': status,
            'error': error,
        }
        if not error:
            return render(request, 'poll/status.html', context)

    return render(request, 'poll/failure.html', context)

prev_hash = '0' * 64

def seal(request):

    if request.method == 'POST':

        if (len(models.Vote.objects.all()) % 5 != 0):
            redirect("login")
        else:
            global prev_hash
            transactions = models.Vote.objects.order_by('block_id').reverse()
            transactions = list(transactions)[:5]
            block_id = transactions[0].block_id

            str_transactions = [str(x) for x in transactions]

            merkle_tree = merkleTree.merkleTree()
            merkle_tree.makeTreeFromArray(str_transactions)
            merkle_hash = merkle_tree.calculateMerkleRoot()

            nonce = 0
            timestamp = datetime.datetime.now().timestamp()

            while True:
                self_hash = sha256('{}{}{}{}'.format(prev_hash, merkle_hash, nonce, timestamp).encode()).hexdigest()
                if self_hash[0] == '0':
                    break
                nonce += 1
            
            block = models.Block(id=block_id,prev_hash=prev_hash,self_hash=self_hash,merkle_hash=merkle_hash,nonce=nonce,timestamp=timestamp)
            prev_hash = self_hash
            block.save()
            print('Block {} has been mined'.format(block_id))

    return redirect("vote")

def verify(request):
    if request.method == 'POST':
        block_count = models.Block.objects.count()
        tampered_block_list = []
        verification = ''
        for i in range (1, block_count+1):
            block = models.Block.objects.get(id=i)
            transactions = models.Vote.objects.filter(block_id=i)
            str_transactions = [str(x) for x in transactions]

            merkle_tree = merkleTree.merkleTree()
            merkle_tree.makeTreeFromArray(str_transactions)
            merkle_tree.calculateMerkleRoot()


            if (block.merkle_hash == merkle_tree.getMerkleRoot()):
                continue
            else:
                tampered_block_list.append(i)
                
        if tampered_block_list:
            verification = 'Verification Failed. Following blocks have been tampered {}'.format(tampered_block_list)
        else:
            verification = 'Verification successful. All votes are intact'

    return render(request, 'poll/verification.html', {'verification':verification})


    