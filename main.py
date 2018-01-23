#!/usr/bin/env python
import argparse
import sys
import os.path

def read_twitter(trainfile, evalfiles):
    """Read the twitter train and evalsets

    The returned object contains {train_sents, train_labels, and eval, with paired sents, labels
    """
    class Data: pass
    data = Data()
    # training data
    data.train_sents, data.train_labels = read_file(trainfile)
    print ".. # train sents", len(data.train_sents)
    data.eval = []
    for efile in evalfiles:
        obj = {}
        sents, labels = read_file(efile)
        obj["sents"]=sents
        obj["labels"]=labels
        data.eval.append(obj)
        print ".. # {} sents".format(efile), len(sents)
    print "Twitter data loaded."
    return data

def read_file(filename):
    """Read the file in CONLL format, assumes one token and label per line."""
    sents = []
    labels = []
    with open(filename, 'r') as f:
        curr_sent = []
        curr_labels = []
        for line in f.readlines():
            if len(line.strip()) == 0:
                # sometimes there are empty sentences?
                if len(curr_sent) != 0:
                    # end of sentence
                    sents.append(curr_sent)
                    labels.append(curr_labels)
                    curr_sent = []
                    curr_labels = []
            else:
                token, label = line.split()
                curr_sent.append(unicode(token, 'utf-8'))
                curr_labels.append(label)
    return sents, labels

def write_preds(fname, sents, labels, preds):
    """Writes the output of a sentence in CONLL format, including predictions."""
    f = open(fname, "w")
    assert len(sents) == len(labels)
    assert len(sents) == len(preds)
    for i in xrange(len(sents)):
        write_sent(f, sents[i], labels[i], preds[i])
    f.close()

def write_sent(f, toks, labels, pred = None):
    """Writes the output of a sentence in CONLL format, including predictions (if pred is not None)"""
    for i in xrange(len(toks)):
        f.write(toks[i].encode('utf-8') + "\t" + labels[i])
        if pred is not None:
            f.write("\t" + pred[i])
        f.write("\n")
    f.write("\n")


def synthetic_data():
    """A very simple, three sentence dataset, that tests some generalization."""
    class Data: pass
    data = Data()
    data.train_sents = [
        [ "Obama", "is", "awesome" , "."],
        [ "Michelle", "is", "also", "awesome" , "."],
        [ "Awesome", "is", "Obama", "and", "Michelle", "."]
    ]
    data.train_labels = [
        [ "PER", "O", "ADJ" , "END"],
        [ "PER", "O", "O", "ADJ" , "END"],
        [ "ADJ", "O", "PER", "O", "PER", "END"]
    ]
    data.dev_sents = [
        [ "Michelle", "is", "awesome" , "."],
        [ "Obama", "is", "also", "awesome" , "."],
        [ "Good", "is", "Michelle", "and", "Obama", "."]
    ]
    data.dev_labels = [
        [ "PER", "O", "ADJ" , "END"],
        [ "PER", "O", "O", "ADJ" , "END"],
        [ "ADJ", "O", "PER", "O", "PER", "END"]
    ]
    return data

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REPLACE WITH DESCRIPTION",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    addonoffarg(parser, 'debug', help="debug mode", default=False)
    parser.add_argument("--train", "-t", type=str, default="data/twitter_train.ner", help="train file")
    #dev test-- twitter_dev_test.ner
    #dev(default) -- twitter_dev.ner
    #test -- twitter_test.ner
    """
    twitter_dev.ner.pred not found; skipping 
    twitter_dev_test.ner.pred not found; skipping 
    twitter_test.ner.pred not found; skipping 
    """
    parser.add_argument("--eval", "-e", type=str, nargs='+', default=["data/twitter_dev.ner"], help="evaluation files")
    parser.add_argument("--outdir", "-o", type=str, default=".", help="location of evaluation files")
    # change default tagger here
    parser.add_argument("--tagger", "-T", default="logreg", choices=["logreg", "crf"], help="which tagger to use; change the default to the one you want to use on q 3.2")

    try:
        args = parser.parse_args()
    except IOError as msg:
        parser.error(str(msg))

    data = read_twitter(trainfile=args.train, evalfiles=args.eval)

    import tagger
    if args.tagger == "logreg":
        tagger = tagger.LogisticRegressionTagger()
    elif args.tagger == "crf":
        tagger = tagger.CRFPerceptron()
    else:
        sys.stderr.write("Did not properly select tagger!")
        sys.exit(1)

    # Train the tagger
    tagger.fit_data(data.train_sents, data.train_labels)

    # Evaluation (also writes out predictions)
    trainoutfile = "{}/{}.pred".format(args.outdir, os.path.basename(args.train))
    print "### Train evaluation; writing to {}".format(trainoutfile)
    data.train_preds = tagger.evaluate_data(data.train_sents, data.train_labels)
    write_preds(trainoutfile, data.train_sents, data.train_labels, data.train_preds)
    for evalstr, evalset in zip(args.eval, data.eval):
        evaloutfile = "{}/{}.pred".format(args.outdir, os.path.basename(evalstr))
        print "### evaluation of {}; writing to {}".format(evalstr, evaloutfile)
        preds = tagger.evaluate_data(evalset["sents"], evalset["labels"])
        write_preds(evaloutfile, evalset["sents"], evalset["labels"], preds)

