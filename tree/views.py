import json
from datetime import *
from django.http import JsonResponse
from utils.models.chatgpt import ChatGPT
from utils.prompts.prompt_config import retrieve_prompt_prefix
from .models import Tree, Knowledge, Graph, Key, Distractor, Question
from user.models import User

# Create your views here.


def gen_list_from_text(text):
    result_list = []
    for result in text.split("- "):
        if len(result) <= 0:
            continue
        result_list.append(
            result.lower() if result[-1] != "\n" else result[:-1].lower())
    return result_list


def index(request):
    return JsonResponse({'code': 200, 'data': "Hello"}, status=200)


def create_knowledge_component(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if "cache" in body:
                cache = body["cache"]
            else:
                cache = True
            concept = body["concept"].lower()
            level = body["level"].lower()
            field = body["field"].lower()
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        old_cache = Knowledge.objects.filter(concept=concept,
                                             level=level,
                                             field=field).first()
        if old_cache and cache:
            ideation = old_cache.ideation
            knowledge = old_cache.knowledge
        else:
            chat_gpt = ChatGPT()
            # stage 1: create ideation content
            prompt = retrieve_prompt_prefix("instructions")["ideation"]
            prompt = prompt.replace("<concept>", concept)
            prompt = prompt.replace("<field>", field)
            prompt = prompt.replace("<level>", level)
            definition = retrieve_prompt_prefix("taxonomy")[level]
            prompt = prompt.replace("<definition>", definition)
            ideation = chat_gpt.call(prompt)
            # stage 2: create knowledge content
            prompt = retrieve_prompt_prefix("instructions")["knowledge"]
            prompt = prompt.replace("<concept>", concept)
            prompt = prompt.replace("<filed>", field)
            prompt = prompt.replace("<level>", level)
            prompt = prompt.replace("<ideation>", ideation)
            knowledge = chat_gpt.call(prompt)
            new_cache = Knowledge(concept=concept,
                                  level=level,
                                  field=field,
                                  ideation=ideation,
                                  knowledge=knowledge,
                                  datetime=datetime.utcnow())
            new_cache.full_clean()
            new_cache.save()
        return JsonResponse(
            {
                'code': 200,
                'data': {
                    'ideation': ideation,
                    'knowledge': knowledge,
                }
            },
            status=200)


def create_knowledge_graph(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if "cache" in body:
                cache = body["cache"]
            else:
                cache = True
            concepts = body["concepts"]
            field = body["field"]
            knowlegde = body["knowledge"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)

        concept_text = ""
        for concept_item in concepts:
            concept_text += concept_item.lower()
            if concept_item != concepts[-1]:
                concept_text += ", "
        knowledge_text = ""
        for knowlegde_item in knowlegde:
            knowledge_text += knowlegde_item + "\n"

        old_cache = Graph.objects.filter(
            concept_text=concept_text,
            field=field,
            knowledge_text=knowledge_text).first()
        graph_text = ""

        if old_cache and cache:
            graph_text = old_cache.graph_text
        else:
            chat_gpt = ChatGPT()
            prompt = retrieve_prompt_prefix("instructions")["graph"]
            prompt = prompt.replace("<concept>", concept_text)
            prompt = prompt.replace("<field>", field)
            prompt = prompt.replace("<text>", knowledge_text)
            graph_text = chat_gpt.call(prompt)
            new_cache = Graph(concept_text=concept_text,
                              field=field,
                              knowledge_text=knowledge_text,
                              graph_text=graph_text,
                              datetime=datetime.utcnow())
            new_cache.full_clean()
            new_cache.save()

        graph = []
        for graph_item in graph_text.split("\n"):
            source = graph_item.split(" | ")[0].split("| ")[-1]
            target = graph_item.split(" | ")[1]
            relation = graph_item.split(" | ")[2].split(" |")[0]
            graph.append({
                "source": source,
                "target": target,
                "relation": relation
            })

        return JsonResponse(
            {
                'code': 200,
                'data': {
                    'graph': graph,
                    'result': graph_text,
                }
            },
            status=200)


def create_key_statement(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if "cache" in body:
                cache = body["cache"]
            else:
                cache = True
            source = body["source"]
            target = body["target"]
            label = body["label"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        old_cache = Key.objects.filter(source=source,
                                       label=label,
                                       target=target).first()

        if old_cache and cache:
            key = old_cache.key
        else:
            prompt = retrieve_prompt_prefix("instructions")["key"]
            prompt = prompt.replace("<source>", source)
            prompt = prompt.replace("<target>", target)
            prompt = prompt.replace("<label>", label)
            chat_gpt = ChatGPT()
            key = chat_gpt.call(prompt)
            new_cache = Key(source=source,
                            label=label,
                            target=target,
                            key=key,
                            datetime=datetime.utcnow())
            new_cache.full_clean()
            new_cache.save()

    return JsonResponse({'code': 200, 'data': {'key': key}}, status=200)


def create_distractor_statement(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if "cache" in body:
                cache = body["cache"]
            else:
                cache = True
            source = body["source"]
            label = body["label"]
            target = body["target"]
            template = body["template"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        old_cache = Distractor.objects.filter(source=source,
                                              label=label,
                                              target=target,
                                              template=template).first()
        if old_cache and cache:
            key = old_cache.key
            heuristics = old_cache.heuristics
            distractors = old_cache.distractors
        else:
            chat_gpt = ChatGPT()
            # stage 1: create keys
            key_prompt = retrieve_prompt_prefix("instructions")["key"]
            key_prompt = key_prompt.replace("<source>", source)
            key_prompt = key_prompt.replace("<target>", target)
            key_prompt = key_prompt.replace("<label>", label)
            key = chat_gpt.call(key_prompt)
            # stage 1: create heuristics
            heuristics_prompt = retrieve_prompt_prefix(
                "instructions")["heuristics"]
            heuristics_prompt = heuristics_prompt.replace("<key>", key)
            heuristics_prompt = heuristics_prompt.replace("<source>", source)
            heuristics_prompt = heuristics_prompt.replace("<label>", label)
            heuristics_prompt = heuristics_prompt.replace("<target>", target)
            heuristics_prompt = heuristics_prompt.replace(
                "<template>", template)
            heuristics = chat_gpt.call(heuristics_prompt)
            # stage 2: create distractors
            distractors_prompt = retrieve_prompt_prefix(
                "instructions")["distractors"]
            distractors_prompt = distractors_prompt.replace("<key>", key)
            distractors_prompt = distractors_prompt.replace("<source>", source)
            distractors_prompt = distractors_prompt.replace("<label>", label)
            distractors_prompt = distractors_prompt.replace("<target>", target)
            distractors_prompt = distractors_prompt.replace(
                "<heuristics>", heuristics)
            distractors = chat_gpt.call(distractors_prompt)
            new_cache = Distractor(source=source,
                                   label=label,
                                   target=target,
                                   template=template,
                                   key=key,
                                   heuristics=heuristics,
                                   distractors=distractors,
                                   datetime=datetime.utcnow())
            new_cache.full_clean()
            new_cache.save()
        return JsonResponse(
            {
                'code': 200,
                'data': {
                    'key':
                    key,
                    'heuristics':
                    heuristics,
                    'distractors': [
                        distractor.split("- ")[-1]
                        for distractor in distractors.split("\n")
                    ]
                }
            },
            status=200)


def create_question(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if "cache" in body:
                cache = body["cache"]
            else:
                cache = True
            concept = body["concept"].lower()
            field = body["field"].lower()
            level = body["level"].lower()
            qtype = body["type"]
            keys = body["keys"]
            distractors = body["distractors"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)

        key_text = " "
        for key_item in keys:
            key_text += "- " + key_item + "\n"
        distractor_text = " "
        for distractor_item in distractors:
            distractor_text += "- " + distractor_item + "\n"

        old_cache = Question.objects.filter(
            concept=concept,
            field=field,
            level=level,
            qtype=qtype,
            key_text=key_text,
            distractor_text=distractor_text).first()

        if old_cache and cache:
            stem = old_cache.stem
            options = old_cache.options
            answer = old_cache.answer
        else:
            chat_gpt = ChatGPT()
            if (qtype == "Multi-Choice"):
                question_prompt = retrieve_prompt_prefix(
                    "instructions")["multiple-choice"]
            else:
                question_prompt = retrieve_prompt_prefix(
                    "instructions")["true-false"]
            question_prompt = question_prompt.replace("<concept>", concept)
            question_prompt = question_prompt.replace("<field>", field)
            question_prompt = question_prompt.replace("<level>", level)
            if len(keys) > 0:
                keys_part = retrieve_prompt_prefix("instructions")["keys-part"]
                question_prompt = question_prompt.replace(
                    "[keys-part]", keys_part)
                question_prompt = question_prompt.replace("<keys>", key_text)
            else:
                question_prompt = question_prompt.replace("[keys-part]", "")
            if len(distractors) > 0:
                distractors_part = retrieve_prompt_prefix(
                    "instructions")["distractors-part"]
                question_prompt = question_prompt.replace(
                    "[distractors-part]", distractors_part)
                question_prompt = question_prompt.replace(
                    "<distractors>", distractor_text)
            else:
                question_prompt = question_prompt.replace(
                    "[distractors-part]", "")
            question = chat_gpt.call(question_prompt)
            stem = question.split("Question:")[-1].split("\n\nOptions:")[0]
            # options = []
            # for question_item in question.split("Options:")[-1].split(
            #         "\n\nAnswer:")[0].split("\n"):
            #     if len(question_item) > 0:
            #         options.append(question_item)
            # answer = question.split("Answer:")[-1].split("\n")[0]
            stem_prompt = retrieve_prompt_prefix("instructions")["stem"]
            stem_prompt = stem_prompt.replace("<question>", question)
            stem = chat_gpt.call(stem_prompt)
            options_prompt = retrieve_prompt_prefix("instructions")["options"]
            options_prompt = options_prompt.replace("<question>", question)
            options = chat_gpt.call(options_prompt)
            answer_prompt = retrieve_prompt_prefix("instructions")["answer"]
            answer_prompt = answer_prompt.replace("<question>", question)
            answer = chat_gpt.call(answer_prompt)
            new_cache = Question(concept=concept,
                                 field=field,
                                 level=level,
                                 qtype=qtype,
                                 key_text=key_text,
                                 distractor_text=distractor_text,
                                 stem=stem,
                                 options=options,
                                 answer=answer,
                                 datetime=datetime.utcnow())
            new_cache.full_clean()
            new_cache.save()
        return JsonResponse(
            {
                'code': 200,
                'data': {
                    'stem': stem,
                    "options": options,
                    "answer": answer
                }
            },
            status=200)


def create_tree(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            name = body["name"]
            role = body["role"]
            identifier = body["identifier"]
            description = body["description"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)
        user = User.objects.filter(name=name, role=role).first()
        tree = Tree(user=user, description=description, identifier=identifier)
        tree.full_clean()
        tree.save()
        return JsonResponse({
            'code': 200,
            'data': "Creating tree succeeded!"
        },
                            status=200)


def read_tree(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            name = body["name"]
            role = body["role"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)

        user = User.objects.filter(name=name, role=role).first()
        return JsonResponse(
            {
                'code':
                200,
                'data': [{
                    'identifier': tree.identifier,
                    'description': tree.description
                } for tree in Tree.objects.filter(user=user)]
            },
            status=200)


def delete_tree(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            name = body["name"]
            role = body["role"]
            identifier = body["identifier"]
            description = body["description"]
        except ValueError:
            return JsonResponse({
                'code': 400,
                'data': "Format Error"
            },
                                status=400)

        user = User.objects.filter(name=name, role=role).first()
        tree = Tree.objects.filter(user=user,
                                   identifier=identifier,
                                   description=description).first()
        if tree:
            tree.delete()
        return JsonResponse({
            'code': 200,
            'data': "Deleting tree succeeded!"
        },
                            status=200)
