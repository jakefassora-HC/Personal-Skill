#!/usr/bin/env node
'use strict';

const fs = require('fs');

const dictionaries = {
  phrases: {
    'could you please': '',
    'can you please': '',
    'i would like you to': '',
    'i want you to': '',
    'i need you to': '',
    'please provide': 'return',
    'give me': 'return',
    'show me': 'return',
    'help me understand': 'explain',
    'can you explain': 'explain',
    'could you walk me through': 'explain',
    'walk me through': 'explain',
    'tell me about': 'explain',
    'tell me how': 'how to',
    'in the event that': 'if',
    'due to the fact that': 'because',
    'for the purpose of': 'to',
    'in order to': 'to',
    'whether or not': 'whether',
    'with regards to': 'about',
    'in relation to': 'about',
    'take into consideration': 'consider',
    'has the capability to': 'can',
    'is required to': 'must',
    'prior to': 'before',
    'subsequent to': 'after',
    'without using': 'no',
    'do not use': 'no',
    'the goal is to': 'goal:',
    'the objective is to': 'goal:',
    'the purpose is to': 'goal:',
    'the task is to': 'task:',
    'your task is to': 'task:',
    'the output should be': 'output:',
    'the result should be': 'output:',
    'the format should be': 'format:',
    'what is the difference between': 'diff:',
    'what are the differences between': 'diff:',
    'make sure to': 'ensure',
    'make sure that': 'ensure',
    'step by step': 'step-by-step',
    'for example': 'e.g.',
    'for instance': 'e.g.',
    'in other words': 'i.e.',
    'it is important to note that': 'note:',
    'please note that': 'note:',
    'in summary': 'summary:',
    'in conclusion': 'conclusion:',
    'in short': 'tldr:'
  },
  logic: {
    'strictly equals': '===',
    'is equal to': '==',
    'does not equal': '!=',
    'greater than or equal to': '>=',
    'less than or equal to': '<=',
    'greater than': '>',
    'less than': '<',
    'logical and': '&&',
    'logical or': '||',
    'is not null': '!= null',
    'is null': '== null',
    'maps to': '=>'
  },
  synonyms: {
    application: 'app',
    repository: 'repo',
    repositories: 'repos',
    directory: 'dir',
    directories: 'dirs',
    database: 'db',
    configuration: 'config',
    configurations: 'configs',
    environment: 'env',
    environments: 'envs',
    architecture: 'arch',
    infrastructure: 'infra',
    kubernetes: 'k8s',
    certificate: 'cert',
    certificates: 'certs',
    deployment: 'deploy',
    deployments: 'deploys',
    pipeline: 'pipe',
    pipelines: 'pipes',
    permission: 'perm',
    permissions: 'perms',
    credential: 'cred',
    credentials: 'creds',
    request: 'req',
    requests: 'reqs',
    response: 'resp',
    responses: 'resps',
    error: 'err',
    errors: 'errs',
    authentication: 'auth',
    authorization: 'authz',
    connection: 'conn',
    connections: 'conns',
    context: 'ctx',
    contexts: 'ctxs',
    dependency: 'dep',
    dependencies: 'deps',
    transaction: 'txn',
    transactions: 'txns',
    query: 'qry',
    queries: 'qrys',
    record: 'rec',
    records: 'recs',
    schema: 'sch',
    timestamp: 'ts',
    identifier: 'id',
    identifiers: 'ids',
    function: 'fn',
    functions: 'fns',
    parameter: 'param',
    parameters: 'params',
    argument: 'arg',
    arguments: 'args',
    specification: 'spec',
    specifications: 'specs',
    asynchronous: 'async',
    synchronous: 'sync',
    implementation: 'impl',
    implementations: 'impls',
    initialize: 'init',
    calculate: 'calc',
    temporary: 'tmp',
    previous: 'prev',
    production: 'prod',
    development: 'dev',
    execute: 'exec',
    generate: 'gen',
    remove: 'rm',
    install: 'inst',
    validate: 'vldn',
    transform: 'xform',
    migrate: 'mig',
    optimize: 'optim',
    normalize: 'norm',
    compress: 'zip',
    decompress: 'unzip',
    'pull request': 'pr',
    'pull requests': 'prs',
    'code review': 'cr',
    'command line interface': 'cli',
    'application programming interface': 'api',
    'continuous integration': 'ci',
    'continuous deployment': 'cd',
    'test driven development': 'tdd'
  },
  blacklist: [
    'a', 'an', 'the', 'very', 'really', 'extremely', 'highly', 'completely',
    'totally', 'basically', 'literally', 'actually', 'honestly', 'simply',
    'obviously', 'clearly', 'just', 'well', 'so', 'then', 'please', 'kindly',
    'hello', 'hi', 'hey', 'thanks', 'thank', 'great', 'excellent', 'awesome',
    'nice', 'good', 'okay', 'ok', 'alright', 'sure', 'interesting', 'helpful',
    'useful', 'important', 'relevant', 'of course', 'as you know', 'as mentioned'
  ]
};

class Defluffer {
  constructor(dicts) {
    this.phrasesAndLogic = { ...dicts.phrases, ...dicts.logic };
    this.synonyms = dicts.synonyms || {};
    this.blacklist = new Set(dicts.blacklist || []);
  }

  compress(input) {
    let text = input;
    const protectedItems = [];

    text = text.replace(/(```[\s\S]*?```|`[^`]+`|https?:\/\/\S+)/g, (match) => {
      protectedItems.push(match);
      return `PROT${protectedItems.length - 1}PROT`;
    });

    for (const entry of this.blacklist) {
      if (!entry.includes(' ')) continue;
      text = text.replace(new RegExp(`\\b${escapeRegExp(entry)}\\b`, 'gi'), ' ');
    }

    for (const [phrase, replacement] of Object.entries(this.phrasesAndLogic)) {
      text = text.replace(new RegExp(`\\b${escapeRegExp(phrase)}\\b`, 'gi'), () => {
        if (!replacement.trim()) return ' ';
        protectedItems.push(replacement);
        return `PROT${protectedItems.length - 1}PROT`;
      });
    }

    let tokens = text.split(/(\b[a-zA-Z0-9_'-]+\b)/);
    tokens = tokens.map((token) => {
      if (!/^[a-zA-Z0-9_'-]+$/.test(token)) return token;
      if (/^PROT\d+PROT$/.test(token)) return token;
      const lower = token.toLowerCase();
      if (this.blacklist.has(lower)) return '';
      return this.synonyms[lower] || token;
    });

    text = clean(tokens.join(''));

    protectedItems.forEach((item, index) => {
      text = text.split(`PROT${index}PROT`).join(item);
    });

    return clean(text);
  }
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function clean(value) {
  return value.replace(/\s+/g, ' ').replace(/\s+([.,?!;:])/g, '$1').trim();
}

function readInput() {
  const argText = process.argv.slice(2).join(' ');
  if (argText) return argText;
  return fs.readFileSync(0, 'utf8');
}

if (require.main === module) {
  const raw = readInput().trim();
  if (!raw) process.exit(0);
  const compressed = new Defluffer(dictionaries).compress(raw);
  process.stdout.write(compressed + '\n');
}

module.exports = { Defluffer, dictionaries };
