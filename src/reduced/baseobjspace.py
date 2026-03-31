


class W_Root(object):
    """This is the abstract root class of all wrapped objects that live
    in a 'normal' object space like StdObjSpace."""
    __slots__ = ('__weakref__',)
    _must_be_light_finalizer_ = True
    user_overridden_class = False

    def getdict(self, space):
        return None

    def getdictvalue(self, space, attr):
        w_dict = self.getdict(space)
        if w_dict is not None:
            return space.finditem_str(w_dict, attr)
        return None

    def setdictvalue(self, space, attr, w_value):
        w_dict = self.getdict(space)
        if w_dict is not None:
            space.setitem_str(w_dict, attr, w_value)
            return True
        return False

    def deldictvalue(self, space, attr):
        w_dict = self.getdict(space)
        if w_dict is not None:
            try:
                space.delitem(w_dict, space.newtext(attr))
                return True
            except OperationError as ex:
                if not ex.match(space, space.w_KeyError):
                    raise
        return False

    def setdict(self, space, w_dict):
        raise oefmt(space.w_TypeError,
                     "attribute '__dict__' of %T objects is not writable",
                     self)

    # to be used directly only by space.type implementations
    def getclass(self, space):
        # make sure that we never annotate this with access_directly set to
        # True. otherwise every call to getclass (and other methods) has an
        # extra indirection due to a much more complicated function set
        check_not_access_directly(self)
        return space.gettypefor(self.__class__)

    def setclass(self, space, w_subtype):
        raise oefmt(space.w_TypeError,
                    "__class__ assignment: only for heap types")

    def user_setup(self, space, w_subtype):
        raise NotImplementedError("only for interp-level user subclasses "
                                  "from typedef.py")

    def getname(self, space):
        try:
            return space.text_w(space.getattr(self, space.newtext('__name__')))
        except OperationError as e:
            if e.match(space, space.w_TypeError) or e.match(space, space.w_AttributeError):
                return '?'
            raise

    def getaddrstring(self, space):
        # slowish
        w_id = space.id(self)
        w_4 = space.newint(4)
        w_0x0F = space.newint(0x0F)
        i = 2 * HUGEVAL_BYTES
        addrstring = [' '] * i
        while True:
            n = space.int_w(space.and_(w_id, w_0x0F), allow_conversion=False)
            n += ord('0')
            if n > ord('9'):
                n += (ord('a') - ord('9') - 1)
            i -= 1
            addrstring[i] = chr(n)
            if i == 0:
                break
            w_id = space.rshift(w_id, w_4)
        return ''.join(addrstring)

    def getrepr(self, space, info, moreinfo=''):
        addrstring = self.getaddrstring(space)
        return space.newtext("<%s at 0x%s%s>" % (info, addrstring,
                                                 moreinfo))

    def getslotvalue(self, index):
        raise NotImplementedError

    def setslotvalue(self, index, w_val):
        raise NotImplementedError

    def delslotvalue(self, index):
        raise NotImplementedError

    def descr_call_mismatch(self, space, opname, RequiredClass, args):
        if RequiredClass is None:
            classname = '?'
        else:
            classname = wrappable_class_name(RequiredClass)
        raise oefmt(space.w_TypeError,
                    "'%s' object expected, got '%T' instead", classname, self)

    # used by _weakref implemenation

    def getweakref(self):
        return None

    def setweakref(self, space, weakreflifeline):
        raise oefmt(space.w_TypeError,
                    "cannot create weak reference to '%T' object", self)

    def delweakref(self):
        pass

    def clear_all_weakrefs(self):
        """Ensures that weakrefs (if any) are cleared now.  This is
        called by UserDelAction before the object is finalized further.
        """
        lifeline = self.getweakref()
        if lifeline is not None:
            # Clear all weakrefs to this object before we proceed with
            # the destruction of the object.  We detach the lifeline
            # first: if the code following before_del() calls the
            # app-level, e.g. a user-defined __del__(), and this code
            # tries to use weakrefs again, it won't reuse the broken
            # (already-cleared) weakrefs from this lifeline.
            self.delweakref()
            lifeline.clear_all_weakrefs()

    def _finalize_(self):
        """The RPython-level finalizer.

        By default, it is *not called*.  See self.register_finalizer().
        Be ready to handle the case where the object is only half
        initialized.  Also, in some cases the object might still be
        visible to app-level after _finalize_() is called (e.g. if
        there is a __del__ that resurrects).
        """

    def register_finalizer(self, space):
        """Register a finalizer for this object, so that
        self._finalize_() will be called.  You must call this method at
        most once.  Be ready to handle in _finalize_() the case where
        the object is half-initialized, even if you only call
        self.register_finalizer() at the end of the initialization.
        This is because there are cases where the finalizer is already
        registered before: if the user makes an app-level subclass with
        a __del__.  (In that case only, self.register_finalizer() does
        nothing, because the finalizer is already registered in
        allocate_instance().)
        """
        if self.user_overridden_class and self.getclass(space).hasuserdel:
            # already registered by space.allocate_instance()
            if not we_are_translated():
                assert space.finalizer_queue._already_registered(self)
        else:
            if not we_are_translated():
                # does not make sense if _finalize_ is not overridden
                assert self._finalize_.im_func is not W_Root._finalize_.im_func
            space.finalizer_queue.register_finalizer(self)

    def may_unregister_rpython_finalizer(self, space):
        """Optimization hint only: if there is no user-defined __del__()
        method, pass the hint ``don't call any finalizer'' to rgc.
        """
        if not self.getclass(space).hasuserdel:
            from rpython.rlib import rgc
            rgc.may_ignore_finalizer(self)

    # hooks that the mapdict implementations needs:
    def _get_mapdict_map(self):
        return None
    def _set_mapdict_map(self, map):
        raise NotImplementedError
    def _mapdict_read_storage(self, index):
        raise NotImplementedError
    def _mapdict_write_storage(self, index, value):
        raise NotImplementedError
    def _mapdict_storage_length(self):
        raise NotImplementedError
    def _set_mapdict_storage_and_map(self, storage, map):
        raise NotImplementedError


    # -------------------------------------------------------------------
    # cpyext support
    # these functions will only be seen by the annotator if we translate
    # with the cpyext module

    def _cpyext_as_pyobj(self, space):
        from pypy.module.cpyext.pyobject import w_root_as_pyobj
        return w_root_as_pyobj(self, space)

    def _cpyext_attach_pyobj(self, space, py_obj):
        from pypy.module.cpyext.pyobject import w_root_attach_pyobj
        return w_root_attach_pyobj(self, space, py_obj)


    # -------------------------------------------------------------------

    def is_w(self, space, w_other):
        return self is w_other

    def immutable_unique_id(self, space):
        return None

    def buffer_w(self, space, flags):
        w_impl = space.lookup(self, '__buffer__')
        if w_impl is None:
            # cpyext types that may have only old buffer interface
            w_impl = space.lookup(self, '__wbuffer__')
        if w_impl is not None:
            w_result = space.get_and_call_function(w_impl, self,
                                        space.newint(flags))
            if (space.isinstance_w(w_result, space.w_buffer) or
                    space.isinstance_w(w_result, space.w_memoryview)):
                return w_result.buffer_w(space, flags)
        raise BufferInterfaceNotFound

    def readbuf_w(self, space):
        # cpyext types that may have old buffer protocol
        w_impl = space.lookup(self, '__rbuffer__')
        if w_impl is None:
            w_impl = space.lookup(self, '__buffer__')
        if w_impl is not None:
            w_result = space.get_and_call_function(w_impl, self,
                                        space.newint(space.BUF_FULL_RO))
            if (space.isinstance_w(w_result, space.w_buffer) or
                    space.isinstance_w(w_result, space.w_memoryview)):
                return w_result.readbuf_w(space)
        raise BufferInterfaceNotFound

    def writebuf_w(self, space):
        # cpyext types that may have old buffer protocol
        w_impl = space.lookup(self, '__wbuffer__')
        if w_impl is None:
            w_impl = space.lookup(self, '__buffer__')
        if w_impl is not None:
            w_result = space.get_and_call_function(w_impl, self,
                                        space.newint(space.BUF_FULL))
            if (space.isinstance_w(w_result, space.w_buffer) or
                    space.isinstance_w(w_result, space.w_memoryview)):
                return w_result.writebuf_w(space)
        raise BufferInterfaceNotFound

    def charbuf_w(self, space):
        w_impl = space.lookup(self, '__buffer__')
        if w_impl is not None:
            w_result = space.get_and_call_function(w_impl, self,
                                        space.newint(space.BUF_FULL_RO))
            if (space.isinstance_w(w_result, space.w_buffer) or
                    space.isinstance_w(w_result, space.w_memoryview)):
                return w_result.charbuf_w(space)
        raise BufferInterfaceNotFound

    def str_w(self, space):
        self._typed_unwrap_error(space, "string")

    def utf8_w(self, space):
        self._typed_unwrap_error(space, "unicode")

    def convert_to_w_unicode(self, space):
        self._typed_unwrap_error(space, "unicode")

    def bytearray_list_of_chars_w(self, space):
        self._typed_unwrap_error(space, "bytearray")

    def int_w(self, space, allow_conversion=True):
        # note that W_IntObject.int_w has a fast path and W_FloatObject.int_w
        # raises w_TypeError
        w_obj = self
        if allow_conversion:
            w_obj = space.int(self)
        return w_obj._int_w(space)

    def _int_w(self, space):
        self._typed_unwrap_error(space, "integer")

    def float_w(self, space, allow_conversion=True):
        w_obj = self
        if allow_conversion:
            w_obj = space.float(self)
        return w_obj._float_w(space)

    def _float_w(self, space):
        self._typed_unwrap_error(space, "float")

    def uint_w(self, space):
        self._typed_unwrap_error(space, "integer")

    def bigint_w(self, space, allow_conversion=True):
        # note that W_IntObject and W_LongObject have fast paths,
        # W_FloatObject.rbigint_w raises w_TypeError raises
        w_obj = self
        if allow_conversion:
            w_obj = space.long(self)
        return w_obj._bigint_w(space)

    def _bigint_w(self, space):
        self._typed_unwrap_error(space, "integer")

    def _typed_unwrap_error(self, space, expected):
        raise oefmt(space.w_TypeError,
                    "expected %s, got %T object", expected, self)

    def int(self, space):
        w_impl = space.lookup(self, '__int__')
        if w_impl is None:
            self._typed_unwrap_error(space, "integer")
        w_result = space.get_and_call_function(w_impl, self)

        if (space.isinstance_w(w_result, space.w_int) or
            space.isinstance_w(w_result, space.w_long)):
            return w_result
        raise oefmt(space.w_TypeError,
                    "__int__ returned non-int (type '%T')", w_result)

    def ord(self, space):
        raise oefmt(space.w_TypeError,
                    "ord() expected string of length 1, but %T found", self)

    def spacebind(self, space):
        """ Return a version of the object bound to a specific object space
        instance. This is used for objects (like e.g. TypeDefs) that are
        constructed before there is an object space instance. """
        return self

    @not_rpython
    def unwrap(self, space):
        # _____ this code is here to support testing only _____
        return self

    def unpackiterable_int(self, space):
        lst = space.listview_int(self)
        if lst:
            return lst[:]
        return None

    def unpackiterable_float(self, space):
        lst = space.listview_float(self)
        if lst:
            return lst[:]
        return None

    def iterator_greenkey(self, space):
        """ Return something that can be used as a green key in jit drivers
        that iterate over self. by default, it's just the type of self, but
        custom iterators should override it. """
        return space.type(self)

    def iterator_greenkey_printable(self):
        return "?"
