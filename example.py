#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2020 Yoshihiro Tanaka
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__ = "Yoshihiro Tanaka <contact@cordea.jp>"
__date__ = "2020-01-19"

import sys
import frida


def on_message(message, data):
    print(message)


js = """
Java.perform(function() {
    var activity;
    Java.choose('jp.cordea.fridademo.MainActivity', {
        onMatch: function(instance) {
            activity = instance;
        },
        onComplete: function() {}
    });

    var detector = Java.use('jp.cordea.fridademo.Detector');
    detector.detect.overload().implementation = function() {
        return true;
    }

    var fabId = activity.findViewById(0x7f080069);
    var fab = Java.cast(
        fabId.$handle,
        Java.use('com.google.android.material.floatingactionbutton.FloatingActionButton')
    );
    var listener = Java.use('android.view.View$OnClickListener');

    var textViewId = activity.findViewById(0x7f0800de);
    var textView = Java.cast(
        textViewId.$handle,
        Java.use('android.widget.TextView')
    );

    var inputLayout1Id = activity.findViewById(0x7f08007b);
    var inputLayout1 = Java.cast(
        inputLayout1Id.$handle,
        Java.use('com.google.android.material.textfield.TextInputLayout')
    );

    var inputLayout2Id = activity.findViewById(0x7f08007c);
    var inputLayout2 = Java.cast(
        inputLayout2Id.$handle,
        Java.use('com.google.android.material.textfield.TextInputLayout')
    );
    var editText2 = inputLayout2.getEditText();

    var string = Java.use('java.lang.String');

    var count = 1;
    fab.setOnClickListener(Java.registerClass({
        name: 'jp.cordea.fridademo.OnClickListener',
        implements: [listener],
        methods: {
            onClick: function(v) {
                count *= 2
                textView.setText(string.$new(count.toString()));

                var text = inputLayout1.getEditText().getText();
                var editText = Java.cast(
                    editText2.$handle,
                    Java.use('android.widget.TextView')
                );
                editText.setText(text);
                send('click');
            }
        }
    }).$new());
});
"""

process = frida.get_usb_device().attach('Gadget')

script = process.create_script(js)
script.on('message', on_message)
script.load()

sys.stdin.read()
